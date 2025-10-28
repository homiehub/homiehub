from __future__ import annotations

from pathlib import Path
import pandas as pd

from src.ingestion.data_handlers.csv_extractor import read_csv_from_gcs
from src.preprocessing.transform import transform_df
from src.load.upload_cleaned_df_to_gcp import upload_df_to_gcs
from src.utils.logger import setup_logger

logger = setup_logger(__name__)

def run_etl() -> Path:
    logger.info("=" * 60)
    logger.info("Starting ETL Pipeline")
    logger.info("=" * 60)
    try:
        logger.info("Step 1/3: Extracting data from GCS")
        df = read_csv_from_gcs(
            bucket_name="homiehub",
            filename="homiehub_listings.csv",
            service_account_key_path="./GCP_Account_Key.json"
        )
        if not isinstance(df, pd.DataFrame):
                logger.error(f"Expected DataFrame, got {type(df)}")
                raise TypeError(f"Expected DataFrame, got {type(df)}")
        if df.empty:
            logger.error("Raw data is empty, cannot proceed with ETL")
            raise ValueError("Raw data is empty")
        logger.info(f"✓ Extracted {len(df)} rows, {len(df.columns)} columns")
        
        logger.info("Step 2/3: Transforming data")
        tdf = transform_df(df)
        if not isinstance(tdf, pd.DataFrame) or tdf.empty:
                logger.error("Transformation resulted in empty DataFrame")
                raise ValueError("Transformation resulted in empty DataFrame")
        logger.info(f"✓ Transformed to {len(tdf)} rows, {len(tdf.columns)} columns")

        logger.info("Step 3/3: Loading data to GCS")
        out_path = upload_df_to_gcs(
            df=tdf,
            filename="homiehub_listings_processed.csv",
            bucket_name="homiehub",
            service_account_key_path="./GCP_Account_Key.json",
        )
        logger.info(f"✓ Loaded to: gs://homiehub/{out_path}")
        logger.info("=" * 60)
        logger.info("ETL Pipeline Completed Successfully!")
        logger.info("=" * 60)
        return out_path
    except Exception as e:
        logger.error("=" * 60)
        logger.error("ETL Pipeline Failed!")
        logger.error("=" * 60)
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    run_etl()
