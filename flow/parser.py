import re


def parse_verification_result(output: str):
    match = re.search(r"RESULT\s*:\s*(PASS|FAIL)", output)

    if match:
        return match.group(1)

    return None
