from google.cloud import storage
from datetime import datetime
import os
import io
from pathlib import Path

def upload_df_to_gcs(df, filename, bucket_name, service_account_key_path, folder="cleaned"):
    """
    Upload a pandas DataFrame directly to GCS as CSV
    
    Args:
        df: pandas DataFrame to upload
        filename: Name for the CSV file (e.g., 'homiehub_listings_processed.csv')
        bucket_name: Name of GCS bucket (e.g., 'homiehub')
        service_account_key_path: Path to your service account JSON key
        folder: Folder name (default: 'processed')
    """
    # Convert to absolute path and set credentials
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = service_account_key_path
    
    # Get today's date in YYYY-MM-DD format
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Create destination path: folder/YYYY-MM-DD/filename.csv
    destination_blob_name = f"{folder}/{today}/{filename}"
    
    # Initialize storage client
    storage_client = storage.Client()
    
    # Get bucket
    bucket = storage_client.bucket(bucket_name)
    
    # Create blob
    blob = bucket.blob(destination_blob_name)
    
    # Convert DataFrame to CSV string
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_string = csv_buffer.getvalue()
    
    # Upload the CSV string
    blob.upload_from_string(csv_string, content_type='text/csv')
    
    print(f"✓ DataFrame uploaded successfully!")
    print(f"  Rows: {len(df)}")
    print(f"  Columns: {len(df.columns)}")
    print(f"  GCS: gs://{bucket_name}/{destination_blob_name}")
    
    return destination_blob_name