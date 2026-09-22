import json
from dataclasses import asdict
from pathlib import Path

from flow.result import RunResult


def save_result(result: RunResult, path: str = "reports/latest.json"):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(asdict(result), file, indent=2)

    return output_path


def save_regression_result(result, path: str = "reports/regression_latest.json"):
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "regression_id": result.regression_id,
        "total": result.total,
        "passed": result.passed,
        "failed": result.failed,
        "status": result.status,
        "cases": [asdict(case) for case in result.cases],
    }

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return output_path
