from dataclasses import dataclass


@dataclass
class RunConfig:
    dut: str = "arbiter"
    simulator: str = "icarus"
    test: str = "basic"
    seed: int = 1
