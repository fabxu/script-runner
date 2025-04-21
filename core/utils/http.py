import requests

from core import constant
from core.auth.auth import Auth
from core.core_beans import NotifyRequest
from core.errors.error import Error, ErrorCode
from core.utils.log import logger


def _getByNewToken(url, auth: Auth, param: dict = None) -> (Error, dict):
    err, token = token = auth.getToken(force=True)
    headers = {}
    if err.code == ErrorCode.SUCCESS:
        headers["token"] = token
    else:
        return err, {}
    rsp = requests.get(url=url, headers=headers, param=param)
    if rsp.status_code == constant.HTTP_CODE_SUCCESS:
        resp = None
        try:
            resp = rsp.json()
        except Exception as e:
            logger.error(f"err in response: {str(e)}")
        if resp is None:
            msg = f"get: {url} failed, No body"
            code = ErrorCode.REQUEST_ERROR
            logger.error(msg)
        else:
            if constant.HTTP_KEY_CODE in resp:
                errorCode = resp[constant.HTTP_KEY_CODE]
                if errorCode == "":
                    result = resp[constant.HTTP_KEY_DATA]
                else:
                    msg = f"get: {url} failed! Code : {errorCode}, msg: {resp[constant.HTTP_KEY_MSG]}"
                    code = ErrorCode.REQUEST_ERROR
                    logger.error(msg)
            else:
                msg = f"get: {url} failed! body: {resp}"
                code = ErrorCode.REQUEST_ERROR
                logger.error(msg)
    else:
        msg = f"get: {url} failed, status_code: {rsp.status_code}"
        code = ErrorCode.REQUEST_ERROR
        logger.error(msg)
    return Error(code, msg), result


def get(url, auth: Auth = None, param: dict = None) -> (Error, dict):
    headers: dict = {}
    result: dict = {}
    if auth is not None:
        err, token = auth.getToken()
        if err.code == ErrorCode.SUCCESS:
            headers["token"] = token
            headers["space"] = str(auth.spaceId)
            headers["X-Auth-User"] = "{\"id\":999999,\"userName\":\"admin\",\"isRoot\":1}"
        else:
            return err, result
    rsp = requests.get(url=url, headers=headers, params=param)
    code, msg = ErrorCode.SUCCESS, "Success"
    if rsp.status_code == constant.HTTP_CODE_SUCCESS:
        resp = None
        try:
            resp = rsp.json()
        except Exception as e:
            logger.error(f"err in response: {str(e)}")
        if resp is None:
            msg = f"get: {url} failed, No body, param: {param}"
            code = ErrorCode.REQUEST_ERROR
            logger.error(msg)
        else:
            if constant.HTTP_KEY_CODE in resp:
                errorCode = resp[constant.HTTP_KEY_CODE]
                if errorCode == "":
                    result = resp[constant.HTTP_KEY_DATA]
                else:
                    if (errorCode == constant.HTTP_ERROR_NO_AUTH) and (auth is not None):
                        err, result = _getByNewToken(url, auth, param)
                    else:
                        msg = f"get: {url} failed, param: {param}! Code : {errorCode}, msg: {resp[constant.HTTP_KEY_MSG]}"
                        code = ErrorCode.REQUEST_ERROR
                        logger.error(msg)
            else:
                msg = f"get: {url} failed, param: {param}! body: {resp}"
                code = ErrorCode.REQUEST_ERROR
                logger.error(msg)
    else:
        msg = f"get: {url} failed, param: {param}, status_code: {rsp.status_code}"
        code = ErrorCode.REQUEST_ERROR
        logger.error(msg)
    return Error(code, msg), result


def _postByNewToken(url, auth: Auth, param: dict = None) -> (Error, dict):
    err, token = token = auth.getToken(force=True)
    headers = {}
    if err.code == ErrorCode.SUCCESS:
        headers["token"] = token
    else:
        return err, {}
    rsp = requests.get(url=url, headers=headers, json=param)
    if rsp.status_code == constant.HTTP_CODE_SUCCESS:
        resp = None
        try:
            resp = rsp.json()
        except Exception as e:
            logger.error(f"err in response: {str(e)}")
        if resp is None:
            msg = f"post: {url} failed, No body"
            code = ErrorCode.REQUEST_ERROR
            logger.error(msg)
        else:
            if constant.HTTP_KEY_CODE in resp:
                errorCode = resp[constant.HTTP_KEY_CODE]
                if errorCode == "":
                    result = resp[constant.HTTP_KEY_DATA]
                    code = ErrorCode.SUCCESS
                    msg = None
                else:
                    msg = f"post: {url} failed! Code : {errorCode}, msg: {resp[constant.HTTP_KEY_MSG]}"
                    code = ErrorCode.REQUEST_ERROR
                    logger.error(msg)
            else:
                msg = f"post: {url} failed! body: {resp}"
                code = ErrorCode.REQUEST_ERROR
                logger.error(msg)
    else:
        msg = f"post: {url} failed, status_code: {rsp.status_code}"
        code = ErrorCode.REQUEST_ERROR
        logger.error(msg)
    return Error(code, msg), result


def post(url, auth: Auth = None, param: dict = None) -> (Error, dict):
    headers: dict = {}
    result: dict = {}
    if auth is not None:
        err, token = auth.getToken()
        if err.code == ErrorCode.SUCCESS:
            headers["token"] = token
            headers["space"] = str(auth.spaceId)
            headers["X-Auth-User"] = "{\"id\":999999,\"userName\":\"admin\",\"isRoot\":1}"
        else:
            return err, result
    rsp = requests.post(url=url, headers=headers, json=param)
    if rsp.status_code == constant.HTTP_CODE_SUCCESS:
        resp = None
        try:
            resp = rsp.json()
        except Exception as e:
            logger.error(f"err in response: {str(e)}")

        if resp is None:
            msg = f"post: {url} failed, No body, param: {param}"
            code = ErrorCode.REQUEST_ERROR
            logger.error(msg)
        else:
            if constant.HTTP_KEY_CODE in resp:
                errorCode = resp[constant.HTTP_KEY_CODE]
                if errorCode == "":
                    result = resp[constant.HTTP_KEY_DATA]
                    code = ErrorCode.SUCCESS
                    msg = None
                else:
                    if (errorCode == constant.HTTP_ERROR_NO_AUTH) and (auth is not None):
                        err, result = _postByNewToken(url, auth, param)
                    else:
                        msg = f"post: {url} failed, param: {param}! Code : {errorCode}, msg: {resp[constant.HTTP_KEY_MSG]}"
                        code = ErrorCode.REQUEST_ERROR
                        logger.error(msg)
            else:
                msg = f"post: {url} failed, param: {param}! body: {resp}"
                code = ErrorCode.REQUEST_ERROR
                logger.error(msg)
    else:
        msg = f"post: {url} failed, param: {param}, status_code: {rsp.status_code}, detail: {rsp.json()}"
        code = ErrorCode.REQUEST_ERROR
        logger.error(msg)
    return Error(code, msg), result


def notifySSE(sseHost: str, auth: Auth, param: NotifyRequest) -> (Error, dict):
    url = sseHost + constant.SSE_AUTH_BASE_URL + "v1/notify"
    return post(url, auth, param.__dict__)
