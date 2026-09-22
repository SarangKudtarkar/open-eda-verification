from dataclasses import dataclass


@dataclass
class PhaseResult:
    name: str
    status: str
    return_code: int

    @property
    def passed(self):
        return self.status == "PASS"
