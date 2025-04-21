from core.errors.error import Error, ErrorCode
import subprocess

from core.utils.log import logger


def getValue(map: dict, key: str, defaultValue: any) -> any:
    if key in map:
        return map[key]
    else:
        return defaultValue

def _splitBucketAndPath(s3Path: str) -> (str, str):
    bucketAndPath = s3Path.split("s3://")[-1]
    bucket, path = bucketAndPath.split("/", 1)
    return bucket, path

def awsPathToAdsPath(awsPath: str, endpoint: str) -> str:
    template = "s3://{}.{}/{}"
    bucket, path = _splitBucketAndPath(awsPath)
    return template.format(bucket, endpoint, path)

def downloadFromS3(key_profile: str, s3Path: str, savePath: str) -> Error:
    # s3Path format: s3://{bucket_name}.{endpoint_domain}/...
    savePath = savePath + "/"
    cmd = f"ads-cli.sh --profile {key_profile} cp {s3Path} {savePath}"
    logger.info(cmd)
    result = subprocess.run(cmd, shell=True)
    if result.stderr:
        return Error(code=ErrorCode.REQUEST_ERROR, msg=result.stderr)
    if result.returncode != 0:
        return Error(code=ErrorCode.REQUEST_ERROR,
                     msg=f"s3 download failed, return code: {result.returncode}, address: {s3Path}")
    return Error(code=ErrorCode.SUCCESS)


def awsDownloadFromS3(key_profile: str, s3Path: str, savePath: str, endpoint: str, recursive: bool = False) -> Error:
    # s3Path format: s3://{bucket_name}/...
    cmd = f"aws --endpoint-url={endpoint} --profile {key_profile} s3 cp {s3Path} {savePath}"
    if recursive:
        cmd += " --recursive"
    logger.info(cmd)
    result = subprocess.run(cmd, shell=True)
    if result.stderr:
        return Error(code=ErrorCode.REQUEST_ERROR, msg=result.stderr)
    if result.returncode != 0:
        return Error(code=ErrorCode.REQUEST_ERROR,
                     msg=f"aws s3 download failed, return code: {result.returncode}, address: {s3Path}")
    return Error(code=ErrorCode.SUCCESS)


def uploadS3(key_profile: str, upload_path: str, path: str) -> Error:
    # upload_path format: s3://{bucket_name}/....
    cmd = f"ads-cli.sh --profile {key_profile} cp {path} {upload_path}"
    result = subprocess.run(cmd, shell=True)
    if result.stderr:
        return Error(code=ErrorCode.REQUEST_ERROR, msg=result.stderr)
    if result.returncode != 0:
        return Error(code=ErrorCode.REQUEST_ERROR,
                     msg=f"upload s3 failed, return code: {result.returncode}, address: {upload_path}")
    return Error(code=ErrorCode.SUCCESS)
