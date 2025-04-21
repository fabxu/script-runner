from core.context import Context
from core.errors.error import Error, ErrorCode
from core.utils.repo import RepoClient


class BaseRunner:
    def __init__(self):
        pass

    def init(self, ctx: Context):
        pass

    def getID(self) -> str:
        pass

    def process(self, ctx: Context, param: str) -> (Error, dict, dict):
        pass

    # add git repo info if necessary: {repo name} => tuple(git_url, target_dir)
    def _getRepoUrls(self) -> dict:
        return {}

    def fetchOperator(self):
        repo_urls = self._getRepoUrls()
        if repo_urls is not None:
            client = RepoClient()
            for repo_name, repo_info in repo_urls.items():
                url, target_dir = repo_info
                client.pull(url, target_dir)
                if not client.if_successful(repo_name, target_dir):
                    raise Error(ErrorCode.INTERNAL_ERROR, f"fetching operator code error: {url}")
