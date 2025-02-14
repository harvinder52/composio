import os

import langchain_core.agents
import yaml
import json
import datetime
from datasets import load_dataset
from pathlib import Path
from composio_crewai import ComposioToolSet, App
from crewai import Agent, Task
from langchain_openai import AzureChatOpenAI
import logging

from rich.logging import RichHandler

CONFIG_FILE_PATH = "./base_task_config.yaml"
TASK_OUTPUT_PATH = "./task_output"

# Path of the current script
script_path = Path(__file__).resolve()
script_dir = script_path.parent
base_task_config_path = script_dir / Path(CONFIG_FILE_PATH)


# get logger
LOGGER_NAME = "local_workspace"

handler = RichHandler(show_time=False, show_path=False)
handler.setLevel(logging.DEBUG)
logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.propagate = False

'''
    princeton swe bench lite dataset has these fields 
    instance_id: (str) - A formatted instance identifier, usually as repo_owner__repo_name-PR-number.
    patch: (str) - The gold patch, the patch generated by the PR (minus test-related code), that resolved the issue.
    repo: (str) - The repository owner/name identifier from GitHub.
    base_commit: (str) - The commit hash of the repository representing the HEAD of the repository before the solution PR is applied.
    hints_text: (str) - Comments made on the issue prior to the creation of the solution PR’s first commit creation date.
    created_at: (str) - The creation date of the pull request.
    test_patch: (str) - A test-file patch that was contributed by the solution PR.
    problem_statement: (str) - The issue title and body.
    version: (str) - Installation version to use for running evaluation.
    environment_setup_commit: (str) - commit hash to use for environment setup and installation.
    FAIL_TO_PASS: (str) - A json list of strings that represent the set of tests resolved by the PR and tied to the issue resolution.
    PASS_TO_PASS: (str) - A json list of strings that represent tests that should pass before and after the PR application.
'''

repo_name = "pydata/xarray"


def filter_from_repo_name(curr_dataset, repo_name):
    filtered_dataset = curr_dataset.filter(lambda x: x["repo"] == repo_name.strip().lower())
    return filtered_dataset


def get_issues_dataset():
    # Load the SWE-bench dataset
    dev_dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="dev")
    test_dataset = load_dataset("princeton-nlp/SWE-bench_Lite", split="test[:3]")
    # filter by repo-name 
    # test_dataset = filter_from_repo_name(test_dataset, repo_name)

    return test_dataset


def build_issue_description(hints, problem_statement):
    if not problem_statement or not problem_statement.strip():
        raise ValueError("problem statement is empty")
    tmpl = ""
    if hints:
        tmpl = f"Here are few hints to solve the issue described in problem_statement {hints}"
    tmpl += f'''\n\n
    Here is the issue, that you have to solve all ob your own 
    {problem_statement}
    '''
    return tmpl


def run():
    """
    Main function to load and display entries from the SWE-bench lite dataset.
    """
    azure_llm = AzureChatOpenAI(
        azure_endpoint=os.environ.get("azure_endpoint"),
        api_key=os.environ.get("azure_key"),
        model="test",
        model_version="1106-Preview",
        api_version="2024-02-01",
    )
    task_output_dir = script_dir / Path(TASK_OUTPUT_PATH + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
    task_output_logs = task_output_dir / Path("agent_logs.json")
    if not os.path.exists(task_output_dir):
        os.makedirs(task_output_dir)
    composio_toolset = ComposioToolSet()
    base_role = (
        "You are the best programmer. You think carefully and step by step take action."
    )
    goal = "Help fix the given issue / bug in the code. And make sure you get it working. "
    tools = composio_toolset.get_tools(apps=[App.LOCALWORKSPACE, App.CMDMANAGERTOOL, App.HISTORYKEEPER])
    issues = get_issues_dataset()
    agent_logs = {}
    for issue in issues:
        issue_description = build_issue_description(issue["hints_text"],
                                                    issue["problem_statement"])
        repo_name = issue["repo"]
        instance_id = issue["instance_id"]
        patch = issue["patch"]
        base_commit = issue["base_commit"]
        install_commit_id = issue["environment_setup_commit"]
        logger.info(f"starting agent for issue-id: {instance_id}\n"
                    f"issue-description: {issue_description}\n"
                    f"repo_name: {repo_name}\n")
        current_logs = []

        # this is a step_callback function -->
        #           used to store logs of agent actions and responses
        def add_in_logs(step_output):
            # get agent input
            if isinstance(step_output, list):
                if len(step_output) < 1:
                    return
                agent_action_with_tool_out = step_output[0]
                if isinstance(agent_action_with_tool_out[0], langchain_core.agents.AgentAction):
                    agent_action = agent_action_with_tool_out[0]
                    tool_out = None
                    if len(agent_action_with_tool_out) > 1:
                        tool_out = agent_action_with_tool_out[1]
                    current_logs.append({"agent_action": agent_action.json(),
                                         "tool_output": tool_out})
                else:
                    print(type(agent_action_with_tool_out[0]))
            else:
                print("type is not list: ", type(step_output))

        with open(base_task_config_path) as f:
            base_config = yaml.safe_load(f.read())

        issue_added_instruction = base_config["issue_description"].format(issue=issue_description,
                                                                          issue_id=instance_id,)
        backstory_added_instruction = base_config["backstory"].format(repo_name=repo_name,
                                                                      base_commit=base_commit,
                                                                      git_access_token=os.environ.get("GITHUB_ACCESS_TOKEN"),
                                                                      install_commit_id=install_commit_id)

        print("--------------------------------------------------")

        expected_output = "A patch should be generated which fixes the given issue"
        swe_agent = Agent(
            role=base_role,
            goal=goal,
            backstory=backstory_added_instruction,
            verbose=True,
            tools=tools,
            llm=azure_llm,
            memory=True,
            cache=False,
            step_callback=add_in_logs,
        )

        coding_task = Task(
            description=issue_added_instruction,
            agent=swe_agent,
            expected_output=expected_output,
        )
        coding_task.execute()
        agent_logs[instance_id] = current_logs
    with open(task_output_logs, "w") as f:
        f.write(json.dumps(agent_logs))


if __name__ == "__main__":
    run()
