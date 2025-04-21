import json

from core.utils import utils

KEY_NAME = "name"
KEY_ID = "id"
KEY_WORKFLOW_TEMPLATE_ID = "workflowTemplateId"
KEY_WORKFLOW_TEMPLATE_NAME = "workflowTemplateName"
KEY_WORKFLOW_TEMPLATE_VERSION = "workflowTemplateVersion"
KEY_CUSTOM_CONFIG = "customConfig"
KEY_EVAL_OBJECT_SOC = "evalObjectSoc"
KEY_EVAL_OBJECT_VERSION = "evalObjectVersion"
KEY_EVAL_OBJECT_CI = "evalObjectCi"
KEY_INPUT_TYPE = "inputType"
KEY_DATASET_INPUT = "datasetInput"
KEY_BENCH_IDS = "benchIds"
KEY_SCRIPT_INPUT_TYPE = "scriptInputType"
KEY_RELATED_ISSUE = "relatedIssues"
KEY_EVAL_RESULT = "evalResultPath"

KEY_SPACE_ID = "spaceId"
KEY_SPACE_NAME = "spaceName"


class Job:
    def __init__(self, jobId: str, param: dict):
        self.name = utils.getValue(param, KEY_NAME, None)
        self.id = utils.getValue(param, KEY_ID, None)
        self.workflowTemplateId = utils.getValue(param, KEY_WORKFLOW_TEMPLATE_ID, None)
        self.workflowTemplateName = utils.getValue(param, KEY_WORKFLOW_TEMPLATE_NAME, None)
        self.workflowTemplateVersion = utils.getValue(param, KEY_WORKFLOW_TEMPLATE_VERSION, None)
        self.customConfig = utils.getValue(param, KEY_CUSTOM_CONFIG, None)
        self.evalObjectSoc = utils.getValue(param, KEY_EVAL_OBJECT_SOC, None)
        self.evalObjectVersion = utils.getValue(param, KEY_EVAL_OBJECT_VERSION, None)
        self.evalObjectCi = utils.getValue(param, KEY_EVAL_OBJECT_CI, None)
        self.spaceId = utils.getValue(param, KEY_SPACE_ID, None)
        self.spaceName = utils.getValue(param, KEY_SPACE_NAME, None)
        self.inputType = utils.getValue(param, KEY_INPUT_TYPE, None)
        dataset = utils.getValue(param, KEY_DATASET_INPUT, None)
        if dataset is not None:
            self.datasetId = utils.getValue(param, KEY_ID, None)
            self.datesetName = utils.getValue(param, KEY_NAME, None)
        self.scriptInputType = utils.getValue(param, KEY_SCRIPT_INPUT_TYPE, None)
        self.relatedIssues = utils.getValue(param, KEY_RELATED_ISSUE, None)
        self.evalResultsPath = utils.getValue(param, KEY_EVAL_RESULT, None)
        self.jobId = jobId
        self.env: dict = {}
        if len(self.customConfig) > 0:
            self.env = json.loads(self.customConfig)


class NotifyRequest:
    def __init__(self, handleType: int, type: int, message: str = None, data: dict = None):
        self.handleType = handleType
        self.type = type
        self.message = message
        self.data = data
