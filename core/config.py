import yaml

from core.errors.error import Error, ErrorCode
from core.utils import utils

CONFIG_SSE_HOST = "sseHost"
CONFIG_TRUTH_HOST = "truthHost"
CONFIG_SSE_SPACE = "sseSpace"
CONFIG_SIMCASE_CREATOR_HOST = "simcaseCreatorHost"
CONFIG_USER = "user"
CONFIG_ADS_PROFILE = "ads"
CONFIG_SSE_BASE_PATH = "sseBasePath"
CONFIG_WORKFLOWID_RSCLBAG_PARSER = "rsclbagParserWorkflowId"

CONFIG_ADDR = "addr"
CONFIG_PWD = "password"
CONFIG_DB = "db"
CONFIG_PORT = "port"
CONFIG_GROUP = "groupNames"


class RedisConfig:
    def __init__(self, config: dict):
        config = config["redis"]
        self.addr = utils.getValue(config, CONFIG_ADDR, None)
        self.port = utils.getValue(config, CONFIG_PORT, 6379)
        self.pwd = utils.getValue(config, CONFIG_PWD, None)
        self.db = utils.getValue(config, CONFIG_DB, None)
        self.groupNames = utils.getValue(config, CONFIG_GROUP, [])

class Config:
    def __init__(self, env: dict):
        self.sseHost = utils.getValue(env, CONFIG_SSE_HOST, None)
        self.sseSpaceID = utils.getValue(env, CONFIG_SSE_SPACE, None)
        self.truthHost = utils.getValue(env, CONFIG_TRUTH_HOST, None)
        self.simCaseCreatorHost = utils.getValue(env, CONFIG_SIMCASE_CREATOR_HOST, "")
        self.ads = utils.getValue(env, CONFIG_ADS_PROFILE, {})
        self.user = utils.getValue(env, CONFIG_USER, {})
        self.sseBasePath = utils.getValue(env, CONFIG_SSE_BASE_PATH, None)
        self.rsclbagParserWorkflowId = utils.getValue(env, CONFIG_WORKFLOWID_RSCLBAG_PARSER, None)


def parserConfig(configPath: str) -> (Error, dict):
    with open(configPath, "r") as file:
        data = yaml.safe_load(file)
        return Error(ErrorCode.SUCCESS), data
    return Error(ErrorCode.PARSER_ERROR, f"parser config failed, config {configPath}"), nil
