from __future__ import annotations
import click
from pyspark.sql import SparkSession
from .api_tools import APITools
from .ingester import Ingester
from .enricher import Enricher

@click.command()
@click.option("--run-all", is_flag=True, help="Run the entire data pipeline.")
def main(run_all):
    if run_all:
        api = APITools()
        Ingester(api).run()
        spark = SparkSession.builder.appName("brewery-pipeline").getOrCreate()
        enr = Enricher(spark)
        enr.run_silver()
        enr.run_gold()
        spark.stop()
    else:
        print("Use --run-all to execute the full pipeline.")

if __name__ == "__main__":
    main()
