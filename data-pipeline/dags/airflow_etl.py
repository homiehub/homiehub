from datetime import datetime
from pathlib import Path
import sys
import pandas as pd
from airflow import DAG
from airflow.operators.python import PythonOperator

# Add project root to sys.path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.utils.io import get_raw_dataset_path, get_processed_dir
from src.ingestion.data_handlers.csv_extractor import read_raw_listings
from src.preprocessing.transform import transform_df

# --- Step 1: Load Raw Data ---
def load_raw_listings_task():
    raw_path = get_raw_dataset_path()
    df = read_raw_listings(raw_path)
    temp_file = get_processed_dir() / "raw_df_temp.csv"
    df.to_csv(temp_file, index=False)
    return str(temp_file)

# --- Step 2: Transform Data ---
def transform_listings_task(**kwargs):
    ti = kwargs['ti']
    raw_file = ti.xcom_pull(task_ids='load_raw_listings')
    df = pd.read_csv(raw_file)
    tdf = transform_df(df)
    temp_file = get_processed_dir() / "transformed_df_temp.csv"
    tdf.to_csv(temp_file, index=False)
    return str(temp_file)

# --- Step 3: Save Processed Data ---
def save_processed_listings_task(**kwargs):
    ti = kwargs['ti']
    transformed_file = ti.xcom_pull(task_ids='transform_listings')
    df = pd.read_csv(transformed_file)
    out_path = get_processed_dir() / "listings_processed.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")
    return str(out_path)

# --- Step 4: Finalize ETL ---
def finalize_etl_task():
    print("ETL DAG completed successfully.")

# --- Step 5: Push summary to XCom ---
def push_summary_task(**kwargs):
    ti = kwargs['ti']
    try:
        df = pd.read_csv(get_processed_dir() / "listings_processed.csv")
        summary = {"rows_processed": len(df), "status": "success"}
    except Exception as e:
        summary = {"rows_processed": 0, "status": "failed", "error": str(e)}
    ti.xcom_push(key="dag_a_summary", value=summary)

# Default args
default_args = {
    'owner': 'homiehub-team',
    'depends_on_past': False,
    'retries': 1,
}

# DAG definition
with DAG(
    dag_id='etl',
    default_args=default_args,
    description='ETL DAG for HomieHub project',
    start_date=datetime(2025, 10, 28),
    schedule=None,
    catchup=False,
) as dag:

    load_raw = PythonOperator(
        task_id='load_raw_listings',
        python_callable=load_raw_listings_task
    )

    transform = PythonOperator(
        task_id='transform_listings',
        python_callable=transform_listings_task
    )

    save_processed = PythonOperator(
        task_id='save_processed_listings',
        python_callable=save_processed_listings_task
    )

    finalize = PythonOperator(
        task_id='finalize_etl',
        python_callable=finalize_etl_task
    )

    push_summary = PythonOperator(
        task_id="push_summary",
        python_callable=push_summary_task
    )

    # Dependencies
    load_raw >> transform >> save_processed >> finalize >> push_summary
