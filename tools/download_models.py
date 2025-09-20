import json
import os
import time
from pathlib import Path

from filelock import FileLock, Timeout
from huggingface_hub import snapshot_download

MODELS_DIR = "./models"
HF_REPO = "Tobero/bwki2025-lowres-langid-model"
HF_REV = "main"

MARKER = MODELS_DIR / ".hf_snapshot.json"
LOCKFILE = MODELS_DIR / ".download.lock"
LOCK = FileLock(str(LOCKFILE))

ALLOW_PATTERNS = tuple(p for p in os.getenv("HF_ALLOW_PATTERNS", "").split(",") if p.strip())
IGNORE_PATTERNS = tuple(p for p in os.getenv("HF_IGNORE_PATTERNS", "").split(",") if p.strip())


def _is_populated() -> bool:
    if MARKER.exists():
        try:
            meta = json.loads(MARKER.read_text())
            return meta.get("repo") == HF_REPO and meta.get("rev") == HF_REV
        except Exception:
            pass
    housekeeping = {MARKER.name, LOCKFILE.name}
    return any(p for p in MODELS_DIR.iterdir() if p.name not in housekeeping)


def ensure_models(timeout_s: int = 60 * 30) -> None:
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with LOCK.acquire(timeout=timeout_s):
            if _is_populated():
                return
            t0 = time.time()
            kwargs = dict(
                repo_id=HF_REPO,
                revision=HF_REV,
                local_dir=str(MODELS_DIR),
                local_dir_use_symlinks=False,
                max_workers=4,
            )
            if ALLOW_PATTERNS:
                kwargs["allow_patterns"] = ALLOW_PATTERNS
            if IGNORE_PATTERNS:
                kwargs["ignore_patterns"] = IGNORE_PATTERNS

            snapshot_download(**kwargs)

            MARKER.write_text(json.dumps({"repo": HF_REPO, "rev": HF_REV, "ts": int(time.time())}))
            print(f"[models] Ready in {time.time() - t0:.1f}s -> {MODELS_DIR}")
    except Timeout:
        raise RuntimeError("Model download lock timed out")

if __name__ == "__main__":
    ensure_models()