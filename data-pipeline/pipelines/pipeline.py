from pathlib import Path
from src.extraction.whatsapp_data_extraction import extract_housing_listings
from src.ingestion.data_handlers.csv_extractor import read_raw_listings
from src.preprocessing.transform import transform_df
from src.utils.io import get_raw_dataset_path, get_processed_dir
from src.utils.gcs import read_csv_from_gcs, upload_df_to_gcs  # if using GCP
from pathlib import Path

# Extract WhatsApp data
def extract_whatsapp_data():
    input_file = Path("data/raw/_chat.txt")
    extract_housing_listings(str(input_file))
    print("Extracted WhatsApp data -> structured_listings_nlp.csv")
    return Path("structured_listings_nlp.csv")

# Load raw data from GCS (optional)
def load_from_gcs(bucket_name="homiehub", filename="homiehub_listings.csv", service_account_key_path="./GCP_Account_Key.json"):
    df = read_csv_from_gcs(bucket_name=bucket_name, filename=filename, service_account_key_path=service_account_key_path)
    print(f"Loaded {len(df)} rows from {filename} in GCS")
    return df

# Transform data
def transform_data(df=None):
    if df is None:
        raw_path = get_raw_dataset_path()
        df = read_raw_listings(raw_path)
    tdf = transform_df(df)
    print(f"Transformed {len(tdf)} rows")
    return tdf

# Upload processed data to GCS
def upload_to_gcs(tdf, bucket_name="homiehub", filename="homiehub_listings_processed.csv", service_account_key_path="./GCP_Account_Key.json"):
    out_path = upload_df_to_gcs(df=tdf, filename=filename, bucket_name=bucket_name, service_account_key_path=service_account_key_path)
    print(f"Uploaded processed data to GCS -> {out_path}")
    return out_path

# Optional helper to run all steps sequentially
def run_etl_pipeline():
    extract_whatsapp_data()
    df = load_from_gcs()
    tdf = transform_data(df)
    upload_to_gcs(tdf)
    print("ETL pipeline finished successfully!")

# Allow standalone execution
if __name__ == "__main__":
    run_etl_pipeline()
