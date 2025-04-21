import os
import argparse
import traceback

from core.errors.error import ErrorCode
from core.utils.log import logger
from runner_mgr import RunnerMgr


def run(jobID: str, batchID: str, env: str, output: str, sharePath: str, runnerID: str, param: str = None) -> (int, str):
    logger.init()
    current_directory = os.getcwd()

    try:
        runnerMgr = RunnerMgr(str(jobID), batchID, env, output, sharePath, current_directory)
        err = runnerMgr.create()
        if err.code == ErrorCode.SUCCESS:
            err = runnerMgr.process(runnerID, param)
            
        if err.code != ErrorCode.SUCCESS:
            logger.error(f"errorCode: {err.code}, msg: {err.msg}")
        return err.code.value, err.msg
    except BaseException as e:
        logger.error(f"{e}")
        traceback.print_exc()
        return ErrorCode.INTERNAL_ERROR.value, str(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", help="job id to start operator")
    parser.add_argument("--batch_id", help="running batch id")
    parser.add_argument("--env", help="runtime env", choices=["beta", "local", "release"])
    parser.add_argument("--runner_id", help="running batch id")
    parser.add_argument("--param", help="running param in json format")
    parser.add_argument("--output", help="output dir")
    parser.add_argument("--sharePath", help="share dir in workflow")

    args = parser.parse_args()
    job_id = args.job_id
    batch_id = args.batch_id
    env = args.env
    runner_id = args.runner_id
    param = args.param
    output = args.output
    sharePath = args.sharePath

    code, msg = run(job_id, batch_id, env, output, sharePath, runner_id, param=param)
    logger.info(f"running result code: {code}, msg: {msg}")
