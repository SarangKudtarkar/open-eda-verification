from dataclasses import dataclass, field

from flow.phases import PhaseResult


@dataclass
class RunResult:
    dut: str
    simulator: str
    test: str
    seed: int
    return_code: int
    status: str
    run_id: str = ""
    log_path: str = ""
    failure_reason: str = ""
    runtime_seconds: float = 0.0
    phases: list[PhaseResult] = field(default_factory=list)

    @property
    def passed(self):
        return self.status == "PASS"
