from pathlib import Path

import yaml

from flow.regression import RegressionCase


def load_regression_cases(path: str = "tests/regression.yaml"):
    config_path = Path(path)

    if not config_path.exists():
        raise FileNotFoundError(
            f"Regression configuration not found: {config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}

    cases = []

    for entry in config.get("tests", []):
        cases.append(
            RegressionCase(
                name=entry["name"],
                seed=int(entry["seed"]),
                test=entry.get("test", "basic"),
            )
        )

    return cases
