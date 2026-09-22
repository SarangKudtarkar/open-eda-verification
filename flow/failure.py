def classify_failure(
    stdout: str,
    stderr: str,
    return_code: int,
    verification_result: str | None = None,
):
    output = f"{stdout}\n{stderr}".lower()

    if return_code == 0 and verification_result == "PASS":
        return "PASS"

    if "scoreboard error" in output:
        return "DUT_MISMATCH"

    if "assertion" in output or "assert failed" in output:
        return "SVA_FAILURE"

    if "timeout" in output:
        return "TIMEOUT"

    if "syntax error" in output or "error:" in output:
        return "COMPILE_OR_SIM_ERROR"

    if verification_result == "FAIL":
        return "VERIFICATION_FAILURE"

    if return_code != 0:
        return "UNKNOWN_FAILURE"

    return "NO_VERIFICATION_RESULT"
