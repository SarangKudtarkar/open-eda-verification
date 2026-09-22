import subprocess
from dataclasses import dataclass


@dataclass
class CommandResult:
    command: list[str]
    return_code: int
    stdout: str
    stderr: str

    @property
    def passed(self):
        return self.return_code == 0


def run_command(command: list[str], env=None):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        env=env,
    )

    return CommandResult(
        command=command,
        return_code=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )
