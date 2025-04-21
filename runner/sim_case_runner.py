from core import constant
from core.constant import NotifyType
from core.context import Context
from core.core_beans import NotifyRequest
from core.errors.error import Error, ErrorCode
from core.runner import BaseRunner
from core.utils import http
from core.utils.log import logger
from runner.bean.beans import ID_BATCH_ID
from runner.runner_const import SimType

import time

SIM_CASE_ENDPOINT = ""

class SimCaseRunner(BaseRunner):
    def __init__(self):
        pass

    def init(self, ctx: Context):
        pass

    def getID(self):
        return constant.ID_SIM_CASE

    def process(self, ctx: Context, param: str) -> (Error, dict, dict):
        err: Error = Error(ErrorCode.SUCCESS)

        logger.error(f"{ctx.sharedData}")
        if "results" in ctx.sharedData:
            cases = ctx.sharedData["results"]
            results = {ID_BATCH_ID: int(ctx.batchID)}
            result: dict = {}
            if (cases is not None) and (len(cases) > 0):
                for key, item in cases.items():
                    simCaseUUID = item["uuid"]
                    simCasePath = item["path"]
                    errMsg = item.get("message", "")
                    data = {
                        "uuid": simCaseUUID, 
                        "path": simCasePath, 
                        "message": errMsg,
                        "status": item["status"],
                        "logPath": item.get("logPath", ""),
                        "endpoint": SIM_CASE_ENDPOINT,
                        "updatedAt": item.get("updatedAt", int(time.time()*1000)),
                    }
                    result[key] = data
            retry = 10
            results["results"] = result
            retry_count = 0
            while retry_count < retry:
                notifyParam = NotifyRequest(NotifyType.simulation.value, SimType.typeSimCaseFinish.value,
                                            data=results)
                err, res = http.notifySSE(ctx.config.sseHost, ctx.auth, notifyParam)
                if err.code != ErrorCode.SUCCESS:
                    logger.error(f"sim case notify sse fail, err: {err}")
                    time.sleep(10)
                    retry_count += 1
                else:
                    break
        return err, None, None
