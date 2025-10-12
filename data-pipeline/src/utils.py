from __future__ import annotations
import json, os, time, logging
from pathlib import Path
from typing import Any, Dict

DEFAULT_DATA_DIR = Path(os.getenv("BREWERY_DATA_DIR", "data")).resolve()
DEFAULT_LOGS_DIR = Path(os.getenv("BREWERY_LOGS_DIR", "logs")).resolve()

INFO_LOG = DEFAULT_LOGS_DIR / "breweries_info.log.jsonl"
ERROR_LOG = DEFAULT_LOGS_DIR / "breweries_error.log.jsonl"

class JsonlFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "level": record.levelname,
            "msg": record.getMessage(),
            "module": record.module,
            "func": record.funcName,
        }
        if record.exc_info:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)

def get_logger(name: str = "breweries") -> logging.Logger:
    DEFAULT_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)

    info_handler = logging.FileHandler(INFO_LOG, encoding="utf-8")
    err_handler = logging.FileHandler(ERROR_LOG, encoding="utf-8")
    fmt = JsonlFormatter()
    info_handler.setFormatter(fmt)
    err_handler.setFormatter(fmt)
    err_handler.setLevel(logging.ERROR)

    logger.addHandler(info_handler)
    logger.addHandler(err_handler)

    stream = logging.StreamHandler()
    stream.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    logger.addHandler(stream)
    return logger

def utc_version() -> str:
    return str(int(time.time()))
