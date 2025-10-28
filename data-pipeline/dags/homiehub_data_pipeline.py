# HomieHub Data Pipeline DAG
# ===================================================== 
# This Airflow DAG performs the end-to-end ETL process for the HomieHub project.
# It includes data extraction, transformation, saving, summarization, and email
# notification of the ETL results.

# Import necessary modules and libraries
from datetime import datetime
from pathlib import Path
import sys
import pandas as pd
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.utils.email import send_email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import glob

# Add project root to sys.path to allow imports from the src directory
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from src.utils.io import get_raw_dataset_path, get_processed_dir
from src.ingestion.data_handlers.csv_extractor import read_raw_listings
from src.preprocessing.transform import transform_df

# ========== STEP 1: Load Raw Data ==========
# Reads the raw housing listings CSV and stores a temporary copy for processing
def load_raw_listings_task():
    raw_path = get_raw_dataset_path()
    df = read_raw_listings(raw_path)
    temp_file = get_processed_dir() / "raw_df_temp.csv"
    df.to_csv(temp_file, index=False)
    return str(temp_file)

# ========== Step 2: Transform Data ========== 
# Applies preprocessing and transformation to the raw dataset
def transform_listings_task(**kwargs):
    ti = kwargs['ti']
    raw_file = ti.xcom_pull(task_ids='load_raw_listings')
    df = pd.read_csv(raw_file)
    tdf = transform_df(df)
    temp_file = get_processed_dir() / "transformed_df_temp.csv"
    tdf.to_csv(temp_file, index=False)
    return str(temp_file)

# ==========  Step 3: Save Processed Data ========== 
# Writes the transformed dataset to a final processed CSV file
def save_processed_listings_task(**kwargs):
    ti = kwargs['ti']
    transformed_file = ti.xcom_pull(task_ids='transform_listings')
    df = pd.read_csv(transformed_file)
    out_path = get_processed_dir() / "listings_processed.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")
    return str(out_path)

# ========== Step 4: Finalize ETL ========== 
# Marks the ETL pipeline completion in logs
def finalize_etl_task():
    print("ETL DAG completed successfully.")

# ========== Step 5: Push summary to XCom ========== 
# Generates a summary of processed rows and ETL status for downstream tasks
def push_summary_task(**kwargs):
    ti = kwargs['ti']
    try:
        df = pd.read_csv(get_processed_dir() / "listings_processed.csv")
        summary = {"rows_processed": len(df), "status": "success"}
    except Exception as e:
        summary = {"rows_processed": 0, "status": "failed", "error": str(e)}
    ti.xcom_push(key="etl_summary", value=summary)
    return summary  # return for next task

# ==========  Step 6: Send Email Notification ========== 
# Sends an email with ETL summary or error details
def send_email_task(**kwargs):
    ti = kwargs['ti']
    summary = ti.xcom_pull(task_ids='push_summary', key='etl_summary')

    if summary is None:
        subject = "ETL Summary Missing"
        html = "<p>No summary found from ETL DAG.</p>"
    elif summary["status"] == "success":
        subject = "ETL Completed Successfully"
        html = f"<p>ETL DAG processed {summary['rows_processed']} rows successfully!</p>"
    else:
        subject = "ETL Failed"
        html = f"<p>ETL DAG failed with error: {summary.get('error', 'Unknown')}</p>"

    send_email(
        to="samhita.kolluri@gmail.com",
        subject=subject,
        html_content=html
    )

# ========== Step 7: Send Logs Email ========== 
# Sends an email with all log files from the current DAG run as attachments
def send_logs_email_task(**kwargs):
    
    # Get DAG run info
    dag_run = kwargs.get('dag_run')
    run_id = dag_run.run_id if dag_run else "manual_run"

    # Base log path
    base_log_dir = Path(__file__).resolve().parents[1] / "logs" / f"dag_id=homiehub_data_pipeline" / f"run_id={run_id}"

    # Collect all log files in the run directory
    log_files = list(base_log_dir.rglob("*.log")) if base_log_dir.exists() else []

    if not log_files:
        print(f"No log files found in {base_log_dir}. Skipping log email.")
        return

    # Prepare email
    subject = f"ETL Logs for DAG run {run_id}"
    body = f"Attached are all log files for DAG run {run_id}."
    to_email = "samhita.kolluri@gmail.com"

    # Send email using Airflow's send_email utility
    send_email(
        to=to_email,
        subject=subject,
        html_content=f"<p>{body}</p>",
        files=[str(f) for f in log_files]
    )

# Default arguments for DAG tasks
default_args = {
    'owner': 'homiehub-team',
    'depends_on_past': False,
    'retries': 1,
}

# ==========  DAG definition ========== 
# Single DAG combining ETL processing and notification tasks
with DAG(
    dag_id='homiehub_data_pipeline',
    default_args=default_args,
    description='ETL DAG with email notification',
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

    notify = PythonOperator(
        task_id="send_email",
        python_callable=send_email_task
    )

    send_logs_email = PythonOperator(
        task_id="send_logs_email",
        python_callable=send_logs_email_task,
        # provide_context=True
    )

    # ========== Define task dependencies to enforce ETL order and notification ========== 
    load_raw >> transform >> save_processed >> finalize >> push_summary >> notify >> send_logs_email