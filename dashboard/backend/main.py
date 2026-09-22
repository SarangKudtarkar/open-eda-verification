from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
from pydantic import BaseModel

from flow.config import RunConfig
from flow.runner import run_verification


BASE_DIR = Path(__file__).resolve().parents[2]
FRONTEND_DIR = BASE_DIR / "dashboard" / "frontend"
ARTIFACTS_DIR = BASE_DIR / "artifacts"


app = FastAPI(
    title="Open EDA Verification",
    version="0.1.0",
)


class RunRequest(BaseModel):
    dut: str = "arbiter"
    simulator: str = "icarus"
    test: str = "basic"
    seed: int = 1


@app.get("/")
def index():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "open-eda-verification",
    }


@app.post("/api/run")
def run(request: RunRequest):
    config = RunConfig(
        dut=request.dut,
        simulator=request.simulator,
        test=request.test,
        seed=request.seed,
    )

    result = run_verification(config)

    return {
        "status": result.status,
        "passed": result.passed,
        "failure_reason": result.failure_reason,
        "runtime_seconds": result.runtime_seconds,
        "run_id": result.run_id,
        "log_path": result.log_path,
    }


@app.get("/api/runs/{run_id}/log", response_class=PlainTextResponse)
def get_run_log(run_id: str):
    run_dir = ARTIFACTS_DIR / run_id
    log_path = run_dir / "simulation.log"

    if not log_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Simulation log not found",
        )

    return log_path.read_text(encoding="utf-8")
