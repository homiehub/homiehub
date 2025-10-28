from __future__ import annotations

from pathlib import Path

from src.ingestion.data_handlers.csv_extractor import read_csv_from_gcs
from src.preprocessing.transform import transform_df
from src.load.upload_cleaned_df_to_gcp import upload_df_to_gcs


def run_etl() -> Path:
    df = read_csv_from_gcs(
        bucket_name="homiehub",
        filename="homiehub_listings.csv",
        service_account_key_path="./GCP_Account_Key.json"
    )
    tdf = transform_df(df)
    out_path = upload_df_to_gcs(
        df=tdf,
        filename="homiehub_listings_processed.csv",
        bucket_name="homiehub",
        service_account_key_path="./GCP_Account_Key.json",
    )
    return out_path


if __name__ == "__main__":
    run_etl()
