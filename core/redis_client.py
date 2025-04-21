from typing import Any

import redis
from redis import Redis
from redis.typing import FieldT

from core.config import RedisConfig
from core.errors.error import Error, ErrorCode


class RedisClient:
    def __init__(self, config: RedisConfig):
        self.client: Redis = redis.Redis(host=config.addr, port=config.port, password=config.pwd, db=config.db)
        self.streamGroups: list = config.groupNames
    
    def initGroup(self, ctx, streamName: str) -> Error:
        streamGroups = [val + f"-{ctx.jobID}-{ctx.batchID}" for val in self.streamGroups]
        err: Error = Error(ErrorCode.SUCCESS)
        # remove group first, avoid group exists error when init group
        try:
            for group in streamGroups:
                self.client.xgroup_destroy(streamName, group)
        except Exception as e:
            # ignore error here if stream or group not exist
            pass

        try:
            for group in streamGroups:
                self.client.xgroup_create(streamName, group, mkstream=True)
        except redis.exceptions.ConnectionError as e:
            err = Error(ErrorCode.CONNECT_ERROR, {e})
        except redis.exceptions.ResponseError as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        except Exception as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        return err

    def destoryStream(self, streamName: str) -> Error:
        err: Error = Error(ErrorCode.SUCCESS)
        try:
            self.client.delete(streamName)
        except redis.exceptions.ConnectionError as e:
            err = Error(ErrorCode.CONNECT_ERROR, {e})
        except redis.exceptions.ResponseError as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        except Exception as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        return err

    def destroyGroup(self, streamName: str, group: str) -> Error:
        err: Error = Error(ErrorCode.SUCCESS)
        try:
            self.client.xgroup_destroy(streamName, group)
        except redis.exceptions.ConnectionError as e:
            err = Error(ErrorCode.CONNECT_ERROR, {e})
        except redis.exceptions.ResponseError as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        except Exception as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        return err

    def ackMessage(self, streamName: str, group: str, id: str) -> Error:
        err: Error = Error(ErrorCode.SUCCESS)
        try:
            self.client.xack(streamName, group, id)
        except redis.exceptions.ConnectionError as e:
            err = Error(ErrorCode.CONNECT_ERROR, {e})
        except redis.exceptions.ResponseError as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        except Exception as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        return err

    def enqueue(self, key: str, values: dict, expire: int = 3600) -> Error:
        err: Error = Error(ErrorCode.SUCCESS)
        try:
            self.client.xadd(key, values)
        except redis.exceptions.ConnectionError as e:
            err = Error(ErrorCode.CONNECT_ERROR, {e})

        except redis.exceptions.ResponseError as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})

        except Exception as e:
            err = Error(ErrorCode.INTERNAL_ERROR, {e})
        self.client.expire(key, expire)
        return err

    def dequeue(self, key: str, group: str, count: int = 5, expire: int = 3600) -> (Error, Any):
        err: Error = Error(ErrorCode.SUCCESS)
        if self.client.exists(key):
            try:
                # read previously pending message first
                messageList = []
                # read pending
                messages = self.client.xreadgroup(group, group, {key: "0"}, count)
                for message in messages:
                    if len(message[-1]) > 0:
                        messageList.append(message[-1][0])
                    
                # read new
                if len(messageList) == 0:
                    messages = self.client.xreadgroup(group, group, {key: ">"}, count)
                    for message in messages:
                        if len(message[-1]) > 0:
                            messageList.append(message[-1][0])
                self.client.expire(key, expire)
                return err, messageList
            except redis.exceptions.ConnectionError as e:
                err = Error(ErrorCode.CONNECT_ERROR, {e})

            except redis.exceptions.ResponseError as e:
                err = Error(ErrorCode.INTERNAL_ERROR, {e})

            except Exception as e:
                err = Error(ErrorCode.INTERNAL_ERROR, {e})
        else:
            err = Error(ErrorCode.NOT_FOUND_ERROR, key + " not found")
        return err, None
