from composio_crewai import App, ComposioToolSet, Action
from crewai import Agent, Crew, Process, Task
from langchain_openai import ChatOpenAI


composio_toolset = ComposioToolSet()

llm = ChatOpenAI(model="gpt-4-turbo")


dev_tools = composio_toolset.get_tools(
    apps=[App.LOCALWORKSPACE, App.CMDMANAGERTOOL, App.HISTORYKEEPER]
)

github_tools = composio_toolset.get_actions(
    actions=[
        Action.GITHUB_GET_CODE_CHANGES_IN_PR,
        Action.GITHUB_PULLS_CREATE,
        Action.GITHUB_PULLS_CHECK_IF_MERGED,
        Action.GITHUB_PULLS_CREATE_REVIEW,
        Action.GITHUB_PULLS_CREATE_REPLY_FOR_REVIEW_COMMENT,
        Action.GITHUB_REPO_S_GET_BRANCH,
        Action.GITHUB_REPO_S_COMPARE_COMMITS,
        Action.GITHUB_REPO_S_GET_COMMIT,
        Action.GITHUB_REPO_S_LIST_BRANCHES,
    ]
)

code_expert_tools = composio_toolset.get_tools(apps=[App.GREPTILE])

if __name__ == "__main__":

    coding_agent = Agent(
        role="Dev Coding Agent",
        goal="Help fix the given issue / bug in the code. And make sure you get it working. ",
        backstory="""
        You are the best programmer. You think carefully and step by step take action.
        You always ask expert agent to help you with your questions.
        You always first collect information from the expert agent, devise your plan and then execute the plan. 
        You have been given access to workspace tool, that allow you to create a workspace and manage files and directories,
        clone your code into a workspace, edit files, run commands on shell.  
        You have to create a workspace only once and can keep using the same workspace for all the tasks. 
        You always think carefully, simplify your questions and provide a clear explaination and examples if possible around the questions. 
        Your answers should be clear and nice. You should make sure you provide extra context and if that means using tools multiple times, that's fine. 
        You have been given access to file, shell manager and workspace manager. You can use them to accomplish your task""",
        verbose=True,
        tools=dev_tools,
        llm=llm,
        memory=True,
        cache=False,
        allow_delegation=True,
    )
    helper_agent = Agent(
        role="Github Helper agent",
        backstory="""
        You are the best helper.
        You think carefully and step by step take action.
        You have github tools to do things like raising a PR and reviewing them. 
        But you can't answer questions about code or code analysis. Code expert agent can help you with that. 
        You might need help from coding agent or expert agent to get things like branch name and commit check. 
        You always think carefully, simplify your questions and provide a clear explaination and examples if possible around the questions. 
        Your answers should be clear and nice. You should make sure you provide extra context and if that means using tools multiple times, that's fine. 
        You have been given access to tools that allow you to control github and query code which can be used for various different code analysis and debugging. 
        """,
        goal="Help the agent to complete the task.",
        verbose=True,
        tools=github_tools,
        llm=llm,
        memory=True,
        cache=False,
        allow_delegation=True,
    )
    expert_agent = Agent(
        role="Code Expert agent",
        backstory="""
        You are the best helper.
        You think carefully and step by step take action.
        You have mentor tool to answer any questions about code. 
        But you only have access to master branch. So any tools you have will not work for other branches or PRs. 
        Your answers should be clear and nice. 
        You should make sure you provide extra context and if that means using tools multiple times, that's fine. 
        You have been given access to tools that allow you to control github and query code which can be used for various different code analysis and debugging""",
        goal="Help the other agents get answers to their questions about code by using the tools you have access to.",
        verbose=True,
        tools=code_expert_tools,
        llm=llm,
        memory=True,
        cache=False,
        allow_delegation=True,
    )

    task1 = Task(
        description="""
        The repo samparkai/composio is python SDK for Composio. 
        You have to check PR#90 for the changes and review them.
        To start off, get the PR changes and decide on questions, that you can ask code expert agent. 
        Code expert can only answer questions around master branch and doesn't have access to other branches and PRs. 
        After you get the answers, you can have more knowledge to give a better review. 
        """,
        agent=coding_agent,
        expected_output="Finalising the questions whose knowledge you want to get from expert agent. Answers to questions are needed for a better review.",
    )
    task2 = Task(
        description="""You help coding agent answer questions about code. 
        You answer all the questions asked by coding agent and help them complete the task.
        If the question is about other branches or PRs, you can't answer it so just say you can't answer that question. 
        """,
        agent=expert_agent,
        context=[task1],
        expected_output="Answer all questions and help the coding agent to get knowledge to write a better review.",
    )
    task3 = Task(
        description="""
        Now you will have all the information you need to write a review for the PR. 
        Write a comprehensive review for the PR, making sure you structure it nicely so that it's easy to understand.
        You can use the information you have from the expert agent to write the review. 
        """,
        agent=coding_agent,
        expected_output="Completed review for the PR that can be posted by helper agent to github",
        context=[task1, task2],
    )
    task4 = Task(
        description="""
        The repo samparkai/composio is python SDK for Composio. 
        You have to check PR#90 for the changes and review them.
        You would have recieved the review from earlier. 
        Please post the review for the PR. 
        """,
        agent=helper_agent,
        expected_output="Successfully posting the review of PR to github",
        context=[task1, task2, task3],
    )

    my_crew = Crew(
        agents=[coding_agent, helper_agent, expert_agent],
        tasks=[task1, task2, task3, task4],
        process=Process.sequential,
        full_output=True,
        verbose=True,
        cache=False,
        memory=True,
    )

    my_crew.kickoff()
    print(my_crew.usage_metrics)
