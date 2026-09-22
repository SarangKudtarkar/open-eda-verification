import os

from flow.artifacts import create_run_directory
from flow.command import run_command
from flow.failure import classify_failure
from flow.config import RunConfig
from flow.phases import PhaseResult
from flow.parser import parse_verification_result
from flow.result import RunResult
from flow.results import save_result
from flow.simulator import get_simulator
from flow.timing import Timer


def run_verification(config: RunConfig):
    print("========================================")
    print("       OPEN EDA VERIFICATION")
    print("========================================")
    print(f"DUT       : {config.dut}")
    print(f"Simulator : {config.simulator}")
    print(f"Test      : {config.test}")
    print(f"Seed      : {config.seed}")
    print("========================================")

    run_id, run_dir = create_run_directory()

    print(f"Run ID    : {run_id}")
    print(f"Run Dir   : {run_dir}")
    print("========================================")

    env = os.environ.copy()
    env["COCOTB_RANDOM_SEED"] = str(config.seed)

    simulator = get_simulator(config.simulator)

    timer = Timer()
    timer.start()

    timer = Timer()
    timer.start()

    command_result = run_command(
        simulator.make_command(),
        env=env,
    )

    timer.stop()
    runtime_seconds = timer.elapsed_seconds

    timer.stop()
    runtime_seconds = timer.elapsed_seconds

    simulation_log = run_dir / "simulation.log"

    with simulation_log.open("w", encoding="utf-8") as file:
        file.write(command_result.stdout)

        if command_result.stderr:
            file.write("\n===== STDERR =====\n")
            file.write(command_result.stderr)

    print(command_result.stdout)

    if command_result.stderr:
        print(command_result.stderr)

    verification_result = parse_verification_result(
        command_result.stdout
    )

    if command_result.return_code != 0:
        status = "FAIL"
    elif verification_result == "PASS":
        status = "PASS"
    else:
        status = "FAIL"

    failure_reason = classify_failure(
        command_result.stdout,
        command_result.stderr,
        command_result.return_code,
        verification_result,
    )

    run_result = RunResult(
        dut=config.dut,
        simulator=config.simulator,
        test=config.test,
        seed=config.seed,
        return_code=command_result.return_code,
        status=status,
        run_id=run_id,
        log_path=str(simulation_log),
        failure_reason=failure_reason,
        runtime_seconds=runtime_seconds,
        phases=[
            PhaseResult(
                name="build",
                status=status,
                return_code=command_result.return_code,
            ),
            PhaseResult(
                name="simulation",
                status=status,
                return_code=command_result.return_code,
            ),
        ],
    )

    save_result(run_result, str(run_dir / "result.json"))
    save_result(run_result, "reports/latest.json")

    print(f"Log       : {simulation_log}")

    return run_result


if __name__ == "__main__":
    config = RunConfig()
    result = run_verification(config)

    print("========================================")
    print(f"RESULT  : {result.status}")
    print(f"REASON  : {result.failure_reason}")
    print(f"PASSED  : {result.passed}")
    print(f"RUNTIME : {result.runtime_seconds:.3f}s")
    print(f"LOG     : {result.log_path}")
    print("========================================")

    raise SystemExit(result.return_code)
