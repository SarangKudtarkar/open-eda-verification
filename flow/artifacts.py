from datetime import datetime
from pathlib import Path


def create_run_directory(base_dir: str = "artifacts"):
    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S_%f")
    run_dir = Path(base_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=False)

    return run_id, run_dir
