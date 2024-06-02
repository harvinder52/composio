from pydantic import Field

from composio.local_tools.local_workspace.commons.get_logger import get_logger
from composio.local_tools.local_workspace.commons.history_processor import (
    history_recorder,
)
from composio.local_tools.local_workspace.commons.local_docker_workspace import (
    communicate,
)
from composio.local_tools.local_workspace.commons.utils import process_output

from .base_class import BaseAction, BaseRequest, BaseResponse


LONG_TIMEOUT = 200
logger = get_logger()


class GithubCloneRequest(BaseRequest):
    repo_name: str = Field(
        default="composio",
        description="""name of github repository to clone. defaults to composio. 
        So if repo overall is meta/react,
        then repo_owner is meta and repo_name is react""",
    )
    repo_owner: str = Field(
        default="samparkai",
        description="""github repository owner. defaults to samparkai. 
        So if repo overall is meta/react,
        then repo_owner is meta and repo_name is react""",
    )


class GithubCloneResponse(BaseResponse):
    pass


class GithubCloneCmd(BaseAction):
    """
    Clones a github repository
    """

    _history_maintains: bool = True
    _display_name = "Clone Github Repository Action"
    _request_schema = GithubCloneRequest
    _response_schema = GithubCloneResponse

    @history_recorder()
    def execute(
        self, request_data: GithubCloneRequest, authorisation_data: dict
    ) -> GithubCloneResponse:
        if not request_data.repo_name or not request_data.repo_name.strip():
            raise ValueError("repo_name can not be null. Give a repo_name to clone")

        import os

        # load github token from env
        github_token = os.getenv("GITHUB_TOKEN")

        if not github_token or not github_token.strip():
            raise ValueError("github_token can not be null")

        self._setup(request_data)

        if self.container_process is None:
            raise ValueError("Container process is not set")

        output, return_code = communicate(
            self.container_process,
            self.container_obj,
            f"git clone https://{github_token}@github.com/{request_data.repo_owner}/{request_data.repo_name}.git && cd {request_data.repo_name}",
            self.parent_pids,
            timeout_duration=LONG_TIMEOUT,
        )
        output, return_code = process_output(output, return_code)
        return GithubCloneResponse(output=output, return_code=return_code)


class GithubCmdRequest(BaseRequest):
    shell_cmd: str = Field(
        ...,
        description="""Shell command to execute, things like git clone, git pull, 
        git commit, git push, git branch, git checkout. 
        The commands cannot be interactive and have to be a single command else it will just fail. 
        Use this to execute any github command directly on shell and make sure to give the full command. 
        """,
    )


class GithubCmdResponse(BaseResponse):
    pass


class GithubCmd(BaseAction):
    """
    Executes a github command directly on shell.
    It also replaces {GITHUB_TOKEN} anywhere in the command with the github token.
    The commands could be anything like git clone, git pull, git commit, git push, git branch, git checkout.
    The commands cannot be interactive and have to be a single command else it will just fail.
    Use this to execute any github command directly on shell and make sure to give the full command.
    """

    _history_maintains: bool = True
    _display_name = "Github Shell Action"
    _request_schema = GithubCmdRequest
    _response_schema = GithubCmdResponse

    @history_recorder()
    def execute(
        self, request_data: GithubCmdRequest, authorisation_data: dict
    ) -> GithubCmdResponse:
        import os

        # load github token from env
        github_token = os.getenv("GITHUB_TOKEN")

        if not github_token or not github_token.strip():
            raise ValueError("github_token can not be null")

        self._setup(request_data)

        if self.container_process is None:
            raise ValueError("Container process is not set")

        output, return_code = communicate(
            self.container_process,
            self.container_obj,
            f"{request_data.shell_cmd.replace('{GITHUB_TOKEN}', github_token)}",
            self.parent_pids,
            timeout_duration=LONG_TIMEOUT,
        )
        output, return_code = process_output(output, return_code)
        return GithubCmdResponse(output=output, return_code=return_code)
