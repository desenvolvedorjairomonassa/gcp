import os
import sys
from datetime import datetime
from pathlib import Path
import pendulum
from airflow.decorators import dag
from airflow.models import Variable
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator
from airflow.utils.trigger_rule import TriggerRule

# Adding the path to the 'scripts' directory
# This allows you to import custom modules from the 'scripts' directory
dag_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(dag_path, "scripts"))

# Global settings
# These are environment variables and paths used throughout the DAG
DAGS_FOLDER = os.environ.get("DAGS")
SUBDIR = f"{DAGS_FOLDER}/order"
SQLDIR = Path("src/sql/merge")

# Loading Airflow variables
# These variables are fetched from Airflow's metadata database
settings = Variable.get("settings", deserialize_json=True)
variables = settings.get("configuration")
TABLE_NAME = "ORDERUMBRELLA"
BUCKET_NAME = variables.get("bucketgcp")
BLOB_NAME = variables.get("buckets3")
PROJECT_ID = "UMBRELLAMARKET"
DATASET_BRONZE = variables.get("dataset_bronze")
DATASET_SILVER = variables.get("dataset_silver")
DATASET_GOLD = variables.get("dataset_gold")
MONTH_ID = variables.get("month_id")
YEAR_ID = variables.get("year_id")

# Macros for use in SQL templates
macros = {
    "bucket": BUCKET_NAME,
    "table": TABLE_NAME,
    "project_id": PROJECT_ID,
    "month_id": MONTH_ID,
    "year_id": YEAR_ID,
    "dataset_bronze": DATASET_BRONZE,
    "dataset_silver": DATASET_SILVER,
    "dataset_gold": DATASET_GOLD,
}

# Default DAG settings
# These settings apply to all tasks in the DAG
DEFAULT_ARGS = {
    "retries": 3,
    "retry_delay": pendulum.duration(minutes=10),
    "email_on_retry": True,
    "owner": "Jairo Monassa",
}

OWNER_LINKS = {
    "Jairo Monassa": "mailto:jairomonassa@cloudumbrella.com"
}

# Helper function to create BigQueryInsertJobOperator operators
# This function simplifies the creation of BigQueryInsertJobOperator tasks
def execute_bigquery_insert_job_operator(
    task_id: str, query_filepath: str | Path, trigger_rule="all_success"
):
    return BigQueryInsertJobOperator(
        task_id=task_id,
        configuration={
            "query": {
                "query": str(query_filepath),
                "useLegacySql": False,
                "priority": "BATCH",
            },
        },
        trigger_rule=trigger_rule,
        location="us-east1",
    )

# DAG definition
@dag(
    dag_id="umbrella.order_to_medallion",
    start_date=pendulum.datetime(2025, 1, 1, 0, 0, 0),
    schedule_interval='0 06 25 3 *',
    catchup=False,
    description="Pipeline architecture integrates S3 to GCP and introduces data medallion layers in BigQuery",
    doc_md="readme.md",
    default_args=DEFAULT_ARGS,
    owner_links=OWNER_LINKS,
    user_defined_macros=macros,
    template_searchpath=SUBDIR,
    tags=["order", "medallion", "bigquery", "s3", "gcp", "bronze", "silver", "gold","UmbrellaCloud"],
)
def storage_to_bigquery():
    blob_name = f"{BLOB_NAME}/{YEAR_ID}/{MONTH_ID}/*.parquet"

    # Loading data from GCS to BigQuery
    # This task loads data from Google Cloud Storage to BigQuery
    load_gcs_to_bq = GCSToBigQueryOperator(
        task_id="load_gcs_to_bq",
        bucket=BUCKET_NAME,
        source_objects=blob_name,
        destination_project_dataset_table=f"{PROJECT_ID}.{DATASET_BRONZE}.{TABLE_NAME}",
        source_format="parquet",
        autodetect=False,
        schema_fields=[
            {
                "name": "OrderID",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "hash ordem"
            },
            {
                "name": "Date",
                "type": "DATE",
                "mode": "REQUIRED",
                "description": "ordem date"
            },
            {
                "name": "Product",
                "type": "STRING",
                "mode": "REQUIRED",
                "description": "product name"
            },
            {
                "name": "Quantity",
                "type": "INTEGER",
                "mode": "REQUIRED",
                "description": "product quantity"
            },
            {
                "name": "UnitPrice",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "unit price"
            },
            {
                "name": "TotalPrice",
                "type": "FLOAT",
                "mode": "REQUIRED",
                "description": "total price from product"
            }
        ],
        write_disposition="WRITE_TRUNCATE",
        create_disposition="CREATE_IF_NEEDED",
        skip_leading_rows=1,
    )

    # Tasks to move data between medallion layers
    task_move_bronze_task = execute_bigquery_insert_job_operator(
        "task_move_bronze", SQLDIR / "merge_into_bronze.sql"
    )

    task_move_silver_task = execute_bigquery_insert_job_operator(
        "task_move_silver", SQLDIR / "merge_into_silver.sql"
    )

    task_move_gold_task = execute_bigquery_insert_job_operator(
        "task_move_gold", SQLDIR / "merge_into_gold.sql"
    )

    # Defining the DAG flow
    # This sets the order in which tasks are executed
    load_gcs_to_bq >> task_move_bronze_task >> task_move_silver_task >> task_move_gold_task

# Instantiating the DAG
dag = storage_to_bigquery()
