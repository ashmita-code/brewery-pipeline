from __future__ import annotations
import json, os, time
from pathlib import Path
from typing import List, Dict
from .api_tools import APITools
from .utils import DEFAULT_DATA_DIR, get_logger, utc_version

logger = get_logger("breweries.ingest")

class Ingester:
    def __init__(self, api: APITools, per_page: int | None = None, retry: int | None = None):
        self.api = api
        self.per_page = per_page or self.api.per_page
        self.retry = int(retry or os.getenv("BREWERY_RETRY", 5))

    def run(self) -> Path:
        version = utc_version()
        bronze_dir = DEFAULT_DATA_DIR / "bronze" / version
        bronze_dir.mkdir(parents=True, exist_ok=True)
        data_fp = bronze_dir / "data.raw"
        failed_fp = bronze_dir / "failed_requests.raw"

        all_ok: List[Dict] = []
        failed_pages: List[int] = []
        page = 1
        while True:
            try:
                data = self.api.fetch_page(page)
                if not data:
                    logger.info(f"No more data at page {page}; stopping.")
                    break
                all_ok.extend(data)
                logger.info(f"Fetched page={page} items={len(data)}")
                page += 1
                time.sleep(0.1)
            except Exception as e:
                logger.error(f"Failed fetching page {page}: {e}")
                failed_pages.append(page)
                page += 1
                time.sleep(0.5)

        with data_fp.open("w", encoding="utf-8") as f:
            json.dump(all_ok, f, ensure_ascii=False)

        still_failed = []
        if failed_pages:
            logger.info(f"Retrying failed pages: {failed_pages}")
            for p in failed_pages:
                ok = False
                for attempt in range(1, self.retry + 1):
                    try:
                        data = self.api.fetch_page(p)
                        if data:
                            all_ok.extend(data)
                        ok = True
                        break
                    except Exception as e:
                        logger.error(f"Retry failed page={p} attempt={attempt}: {e}")
                        time.sleep(0.8)
                if not ok:
                    still_failed.append(p)

        with failed_fp.open("w", encoding="utf-8") as f:
            json.dump(still_failed, f, ensure_ascii=False)

        if still_failed:
            logger.error(f"Ingestion done with failures: {still_failed}")
        else:
            logger.info(f"Ingestion succeeded. Records={len(all_ok)}")
        return bronze_dir
