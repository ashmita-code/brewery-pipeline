from __future__ import annotations
import json
from pathlib import Path
from typing import Dict
from pyspark.sql import SparkSession, functions as F, types as T
from .api_tools import APITools
from .utils import DEFAULT_DATA_DIR, get_logger

logger = get_logger("breweries.enrich")

class Enricher:
    def __init__(self, spark: SparkSession):
        self.spark = spark
        self.api = APITools()

    def _latest_version_dir(self, stage: str) -> Path:
        stage_dir = DEFAULT_DATA_DIR / stage
        versions = sorted([p for p in stage_dir.iterdir() if p.is_dir()], key=lambda p: p.name)
        if not versions:
            raise FileNotFoundError(f"No versions found for '{stage}'")
        return versions[-1]

    def run_silver(self) -> Path:
        bronze_dir = self._latest_version_dir("bronze")
        data_fp = bronze_dir / "data.raw"
        with data_fp.open("r", encoding="utf-8") as f:
            raw = json.load(f)

        cols = [
            "id","name","brewery_type","address_1","city","state_province",
            "postal_code","country","longitude","latitude","phone","website_url"
        ]
        def norm(r: Dict) -> Dict:
            out = {c: (None if r.get(c) in (None, "") else str(r.get(c))) for c in cols}
            return out

        normalized = [norm(r) for r in raw]
        df = self.spark.createDataFrame(normalized)

        for c in df.columns:
            df = df.withColumn(c, F.when(F.col(c).isNull(), F.lit(None)).otherwise(F.trim(F.col(c))))

        df = df.withColumn("longitude", F.col("longitude").cast(T.DoubleType()))
        df = df.withColumn("latitude",  F.col("latitude").cast(T.DoubleType()))

        valid_types = self.api.valid_brewery_types()
        df = df.withColumn(
            "brewery_type",
            F.when(F.col("brewery_type").isin(valid_types), F.col("brewery_type")).otherwise(F.lit("unknown"))
        )

        ordered = [
            "id","name","brewery_type","country","state_province","city",
            "postal_code","address_1","phone","website_url","longitude","latitude"
        ]
        df = df.select(*ordered)

        version = bronze_dir.name
        silver_dir = DEFAULT_DATA_DIR / "silver" / version
        df.repartition("country").write.mode("overwrite").partitionBy("country").parquet(str(silver_dir))
        logger.info(f"Silver written to {silver_dir}")
        return silver_dir

    def run_gold(self) -> Path:
        silver_dir = self._latest_version_dir("silver")
        df = self.spark.read.parquet(str(silver_dir))
        gold = (
            df.groupBy("country","brewery_type")
              .agg(F.count(F.lit(1)).alias("brewery_count"))
              .orderBy("country","brewery_type")
        )
        gold_dir = DEFAULT_DATA_DIR / "gold" / silver_dir.name
        gold.repartition(1).write.mode("overwrite").parquet(str(gold_dir))
        logger.info(f"Gold written to {gold_dir}")
        return gold_dir
