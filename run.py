import argparse

from flow.config import RunConfig
from flow.regression import run_regression
from flow.regression_config import load_regression_cases
from flow.results import save_regression_result
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

    parser.add_argument(
        "--regression",
        action="store_true",
        help="Run the regression suite",
    )

    parser.add_argument(
        "--regression-file",
        default="tests/regression.yaml",
        help="Regression configuration file",
    )

    args = parser.parse_args()

    if args.regression:
        cases = load_regression_cases(args.regression_file)

        result = run_regression(
            cases,
            simulator=args.simulator,
            dut=args.dut,
        )

        report_path = save_regression_result(result)

        print("")
        print("========================================")
        print("REGRESSION SUMMARY")
        print("========================================")
        print(f"Total  : {result.total}")
        print(f"Passed : {result.passed}")
        print(f"Failed : {result.failed}")
        print(f"Status : {result.status}")
        print(f"Report : {report_path}")
        print("========================================")

        raise SystemExit(0 if result.status == "PASS" else 1)

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
