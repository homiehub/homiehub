from pathlib import Path
import pandas as pd
from src.utils.io import get_raw_dataset_path, get_processed_dir
from src.ingestion.data_handlers.csv_extractor import read_raw_listings
from src.preprocessing.transform import transform_df


def load_raw_data() -> pd.DataFrame:
    """
    Step 1: Load raw CSV data into a DataFrame.
    This function reads the raw dataset from the data/raw directory.
    """
    raw_path = get_raw_dataset_path()
    df = read_raw_listings(raw_path)
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Step 2: Transform the raw DataFrame.
    Applies preprocessing and feature engineering to the raw data.
    """
    tdf = transform_df(df)
    return tdf


def save_processed_data(df: pd.DataFrame) -> Path:
    """
    Step 3: Save the transformed DataFrame to the processed directory.
    Outputs the cleaned and structured CSV ready for downstream use.
    """
    out_path = get_processed_dir() / "listings_processed.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df)} rows to {out_path}")
    return out_path


def run_etl() -> Path:
    """
    Step 4: Orchestrator function to run all ETL steps.
    This function sequentially executes data loading, transformation,
    and saving of the processed dataset.
    """
    raw_df = load_raw_data()
    transformed_df = transform_data(raw_df)
    out_path = save_processed_data(transformed_df)
    return out_path


if __name__ == "__main__":
    run_etl()
