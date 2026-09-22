import argparse

from flow.config import RunConfig
from flow.runner import run_verification


def main():
    parser = argparse.ArgumentParser(
        description="Open EDA Verification Runner"
    )

    parser.add_argument(
        "--dut",
        default="arbiter",
        help="DUT to verify",
    )

    parser.add_argument(
        "--simulator",
        default="icarus",
        choices=["icarus", "verilator"],
        help="Simulator backend",
    )

    parser.add_argument(
        "--test",
        default="basic",
        help="Verification test to run",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=1,
        help="Randomization seed",
    )

    args = parser.parse_args()

    config = RunConfig(
        dut=args.dut,
        simulator=args.simulator,
        test=args.test,
        seed=args.seed,
    )

    result = run_verification(config)

    raise SystemExit(result.return_code)


if __name__ == "__main__":
    main()
