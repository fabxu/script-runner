from enum import Enum

FORMAT_TIME = "%Y-%m-%d %H_%M_%S"
CONFIG_ENV_LOCAL = "local"
CONFIG_ENV_BETA = "beta"
CONFIG_ENV_RELEASE = "release"

CONFIG_SUFFIX = "_config.yml"

PATH_SHARED_DATA = "/workflow_shared.json"

HTTP_CODE_SUCCESS = 200
HTTP_CODE_SUCCESS_MESSAGE = "success.ok"

PATH_WORK_DIR = "/workspace/"

HTTP_KEY_CODE = "code"
HTTP_KEY_DATA = "data"
HTTP_KEY_MSG = "message"

HTTP_ERROR_CODE = "success.ok"

HTTP_ERROR_NO_AUTH = "error.auth.sso_verify_failed"

INVALID = -1

ID_BIG_RECYCLE = "bigRecycle"
ID_PERCEPTION_METRIX = "perceptionMetrix"
ID_SIM_CASE = "simCase"
ID_SIM_CASE_GENERATOR = "simCaseGenerator"
ID_GT_DATASET_GENERATOR = "gtDatasetGenerator"

URL_JOB_BATCH_CASE = "/v1/jobcases"
URL_JOB_METRIC = "/v1/metrics"

KEY_LIST = "list"

SSE_NOAUTH_BASE_URL = "/api/sse-service/noauth"
SSE_AUTH_BASE_URL = "/api/sse-service/"

REDIS_KEY_SIMCASE_LIST_NAME = "sse:simcase:{}_{}"

OSS_ENDPOINT = ""


class NotifyType(Enum):
    recycle = 1
    simulation = 2
    perceptionMetric = 3
