from enum import Enum

KEY_RELATED_ID = "relatedId"


class JobSourceType(Enum):
    jobSourceType_None = 0
    jobSourceType_System = 1  # 业务系统
    jobSourceType_Manual = 2  # 手动脚本
    jobSourceType_Dazhuo = 3  # 定时任务
    jobSourceType_Child = 4  # 子任务
    jobSourceType_HTTP = 5  # 接口请求
    jobSourceType_Eval = 6  # 测评

class CreatingSimcaseJobSourceType(Enum):
    jobSourceType_None = "None"
    jobSourceType_SSE = "SSE-Simcase-Generate"  # 评测来源
    jobSourceType_Manual = "Mannual-Simcase-Generate"  # 手动脚本

class TruthJobGtType(Enum):
    laneLine = 405
    pvb = 406
    gop = 407
    recycle = 408


class RecycleType(Enum):
    typeRecycleStart = 1
    typeRecycleFinish = 2
    typeEvaluationMetrixFinish = 3


class JobCaseStatus(Enum):
    JobCase_Default = 0
    JobCase_Success = 1
    JobCase_Recycle_Failed = 2
    JobCase_Simcase_Failed = 3
    JobCase_Recycle_Running = 4
    JobCase_SimCase_Running = 5
    JobCase_Perception_Failed = 6
    JobCase_Perception_Success = 7

class MetricType(Enum):
    Sim = 1
    Perception = 2

class PerceptionConclusion(Enum):
    Perception_conclusion_default = 0
    Perception_conclusion_unknown = 1
    Perception_conclusion_error = 2
    Perception_conclusion_alert = 3
    Perception_conclusion_pass = 4

class SimType(Enum):
    typeSimCaseFinish = 1
    typeSimCaseGenerated = 2

class PerceptionMetricType(Enum):
    typePerceptionFinish = 1
    typePerceptionResultGenerated = 2
    typePerceptionTimeout = 3
