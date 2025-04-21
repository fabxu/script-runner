import redis
import requests

from core import constant
from core.config import Config, CONFIG_USER
from core.errors.error import Error, ErrorCode
from core.redis_client import RedisClient
from core.utils.log import logger

REDIS_KEY_TOKEN = "dataproauth:access:token"
URL_LOGIN = "/api/data/account/login"

SECONDS_OF_HOUR = 3600

class Auth:
    def __init__(self, config: Config):
        self.url = config.sseHost + URL_LOGIN
        self.userInfo = config.user
        self._token = ""
        self.spaceId = config.sseSpaceID

    def init(self, client: RedisClient):
        self.client = client

    def _getToken(self) -> (Error, str):
        token = ""
        rsp = requests.post(url=self.url, json=self.userInfo)
        code = ErrorCode.SUCCESS
        msg = "Success"

        if rsp.status_code == constant.HTTP_CODE_SUCCESS:
            resp = rsp.json()
            if resp is None:
                msg = "login failed, No body"
                code = ErrorCode.REQUEST_ERROR
                logger.error(msg)
            else:
                if constant.HTTP_KEY_CODE in resp:
                    errorCode = resp[constant.HTTP_KEY_CODE]
                    if errorCode == constant.HTTP_CODE_SUCCESS_MESSAGE:
                        token = resp[constant.HTTP_KEY_DATA]
                        self.client.client.set(REDIS_KEY_TOKEN, token, ex=8*SECONDS_OF_HOUR)
                    else:
                        msg = f"login failed! Code : {errorCode}"
                        code = ErrorCode.REQUEST_ERROR
                        logger.error(msg)
                else:
                    msg = "login failed!"
                    code = ErrorCode.REQUEST_ERROR
                    logger.error(msg)
        else:
            msg = f"login failed, status_code: {rsp.status_code}"
            code = ErrorCode.REQUEST_ERROR
            logger.error(msg)
        return Error(code, msg), token

    def getToken(self, force: bool = False) -> (Error, str):
        err = Error(ErrorCode.SUCCESS)
        if force:
            err, self._token = self._getToken()
        else:
            if len(self._token) == 0:
                try:
                    value = self.client.client.get(REDIS_KEY_TOKEN)
                    if value is None:
                        err, self._token = self._getToken()
                    else:
                        self._token = value.decode()

                except redis.RedisError as e:
                    logger.error(f"{e}")
                    err, self._token = self._getToken()

        return err, self._token
