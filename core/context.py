import json
import os
from typing import Any

from core import constant
from core.auth.auth import Auth
from core.config import Config, parserConfig
from core.errors.error import Error, ErrorCode
from core.core_beans import Job
from core.redis_client import RedisClient, RedisConfig
from core.utils import http, flowcli_util
from core.utils.log import logger

PATH_SSE_JOB = "/v1/jobs/"


class Context:
    def __init__(self, jobID: str, batchID: str, env: str, output: str, sharePath: str, curPath: str):
        self.jobID = jobID
        self.batchID = batchID
        self._configName = os.path.join(curPath, env + constant.CONFIG_SUFFIX)
        self.output = output
        self.curPath = curPath
        self.sharePath = sharePath
        self._sharedFile = sharePath + constant.PATH_SHARED_DATA
        self.config: Config = None
        self.redis: RedisClient = None
        self.auth: Auth = None
        self.job: Job = None
        self.sharedData: dict = {}

    def _getJob(self, jobId) -> Error:
        getJobUrl = self.config.sseHost + self.config.sseBasePath + PATH_SSE_JOB + jobId
        err, rsp = http.get(getJobUrl, self.auth)
        if err.code == ErrorCode.SUCCESS:
            self.job = Job(jobId, rsp)
        return err

    def create(self) -> Error:
        err, data = parserConfig(self._configName)
        if err.code == ErrorCode.SUCCESS:
            self.config = Config(data)
            # init auth
            self.auth = Auth(self.config)
            # init redis
            redisConfig = RedisConfig(data)
            self.redis = RedisClient(redisConfig)
            self.auth.init(self.redis)
            self._loadSharedData()
            err = self._getJob(self.jobID)
        logger.error(f"create complete")
        return err

    def _loadSharedData(self):
        if os.path.exists(self._sharedFile):
            with open(self._sharedFile, "r", encoding="utf-8") as f:
                self.sharedData = json.load(f)
                logger.error(f"_loadSharedData: {self.sharedData}")

    def saveSharedData(self, data: dict):
        if (data is not None) and (len(data) > 0):
            self.sharedData.update(data)
            with open(self._sharedFile, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

    def saveData(self, data: dict):
        if (data is not None) and len(data) > 0:
            e = flowcli_util.save(constant.OSS_ENDPOINT, data)
            if e.code != ErrorCode.SUCCESS:
                logger.info(f"flowcli save {e}")

    def getSharedData(self, key: str) -> (Error, Any):
        if key in self.sharedData:
            return Error(ErrorCode.SUCCESS), self.sharedData[key]
        else:
            return Error(ErrorCode.NOT_FOUND_ERROR, msg=f"not found shared data, key: {key}"), None
