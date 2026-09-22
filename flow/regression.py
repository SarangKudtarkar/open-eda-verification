from dataclasses import dataclass, field

from flow.config import RunConfig
from flow.result import RunResult
from flow.runner import run_verification


@dataclass
class RegressionCase:
    name: str
    seed: int
    test: str = "basic"


@dataclass
class RegressionResult:
    regression_id: str = ""
    cases: list[RunResult] = field(default_factory=list)

    @property
    def total(self):
        return len(self.cases)

    @property
    def passed(self):
        return sum(result.passed for result in self.cases)

    @property
    def failed(self):
        return self.total - self.passed

    @property
    def status(self):
        if self.total == 0:
            return "EMPTY"

        if self.failed == 0:
            return "PASS"

        return "FAIL"


def run_regression(
    cases: list[RegressionCase],
    simulator: str = "icarus",
    dut: str = "arbiter",
):
    from flow.artifacts import create_regression_id

    regression_result = RegressionResult(
        regression_id=create_regression_id()
    )

    for case in cases:
        print("")
        print("========================================")
        print(f"REGRESSION CASE : {case.name}")
        print("========================================")

        config = RunConfig(
            dut=dut,
            simulator=simulator,
            test=case.test,
            seed=case.seed,
        )

        result = run_verification(config)
        regression_result.cases.append(result)

    return regression_result
