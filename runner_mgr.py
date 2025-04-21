from core.context import Context
from core.errors.error import ErrorCode, Error
from core.runner import BaseRunner
from core.utils.log import logger
from runner.sim_case_runner import SimCaseRunner

class RunnerMgr:
    def __init__(self, jobID: str, batchID: str, env: str, output: str, sharePath: str, curPath: str):
        self.ctx = Context(jobID, batchID, env, output, sharePath, curPath)
        self.runners: dict = {}

    def create(self) -> Error:
        err = self.ctx.create()
        if err.code == ErrorCode.SUCCESS:
            self._registerRunner(SimCaseRunner())
        logger.error(f"RunnerMgr create complete")
        return err

    def _registerRunner(self, runner: BaseRunner):
        self.runners[runner.getID()] = runner

    def process(self, runnerId: str, param: str) -> Error:
        err = Error(ErrorCode.NOT_FOUND_ERROR, f"not found: {runnerId}")
        logger.error(f"{runnerId} process start")
        if runnerId in self.runners:
            self.runners[runnerId].init(self.ctx)
            logger.error(f"process init")
            self.runners[runnerId].fetchOperator()
            logger.error(f"process fetchOperator")
            logger.error(f"process {param}")
            err, sharedData, saveData = self.runners[runnerId].process(self.ctx, param)
            if err.code == ErrorCode.SUCCESS:
                self.ctx.saveSharedData(sharedData)
                self.ctx.saveData(saveData)
            else:
                logger.error(f"{runnerId} process failed, {err}")

        return err
