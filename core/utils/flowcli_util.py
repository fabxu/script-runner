import subprocess

from core.errors.error import Error, ErrorCode


def save(endpoint: str, result: dict) -> Error:
    if (result is not None) and (len(result) > 0):
        for key, value in result.items():
            cmd = f"flowcli s3 save -e {endpoint} -k {key} -p {value}"
            result = subprocess.run(cmd, shell=True)
            if result.stderr:
                return Error(code=ErrorCode.REQUEST_ERROR, msg=result.stderr)
            if result.returncode != 0:
                return Error(code=ErrorCode.REQUEST_ERROR,
                             msg=f"upload s3 failed, return code: {result.returncode}, address: {key}")
    return Error(ErrorCode.SUCCESS)
