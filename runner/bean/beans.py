from core.utils import utils
from runner.runner_const import TruthJobGtType, JobSourceType

ID_ID = "id"
ID_JOB_ID = "jobId"
ID_BATCH_ID = "batchId"
ID_SEGMENT_ID = "segmentId"
ID_SEGMENT_NAME = "segmentName"
ID_SEGMENT_S3 = "segmentS3"
ID_RECYCLE_ID = "recycleId"
ID_RECYCLE_NAME = "recycleName"
ID_RECYCLE_S3 = "recycleS3"
ID_SIM_CASE_ID = "simcaseId"
ID_SIM_CASE_NAME = "simcaseName"
ID_SIM_CASE_S3 = "simcaseS3"
ID_METRIC_ID = "metricId"


class JobCase:
    def __init__(self, param: dict):
        self.id = utils.getValue(param, ID_ID, 0)
        self.jobId = utils.getValue(param, ID_JOB_ID, 0)
        self.batchId = utils.getValue(param, ID_BATCH_ID, 0)
        self.segmentId = utils.getValue(param, ID_SEGMENT_ID, None)
        self.segmentName = utils.getValue(param, ID_SEGMENT_NAME, None)
        self.segmentName = utils.getValue(param, ID_SEGMENT_NAME, None)
        self.segmentS3 = utils.getValue(param, ID_SEGMENT_S3, None)
        self.recycleId = utils.getValue(param, ID_RECYCLE_ID, None)
        self.recycleName = utils.getValue(param, ID_RECYCLE_NAME, None)
        self.recycleS3 = utils.getValue(param, ID_RECYCLE_S3, None)
        self.simcaseId = utils.getValue(param, ID_SIM_CASE_ID, None)
        self.simcaseName = utils.getValue(param, ID_SIM_CASE_NAME, None)
        self.simcaseS3 = utils.getValue(param, ID_SIM_CASE_S3, None)
        self.metricID = utils.getValue(param, ID_METRIC_ID, "")


class AddTruthJobRequest:
    def __init__(self, gt_type: TruthJobGtType, meta_path: list, job_source_type: JobSourceType):
        self.gt_types = [gt_type.value]
        self.meta_path = meta_path
        self.job_source_type = job_source_type.value

class DatasetItem:
    def __init__(self, case: JobCase):
        self.s3path = case.segmentS3
        self.uuid = case.segmentId
        self.name = case.segmentName
