from __future__ import annotations

from pathlib import Path
# from ..src.utils.io import get_raw_dataset_path, get_processed_dir
# from ..src.ingestion.data_handlers.csv_extractor import read_raw_listings
# from ..src.preprocessing.transform import transform_df
from src.utils.io import get_raw_dataset_path, get_processed_dir
from src.ingestion.data_handlers.csv_extractor import read_raw_listings
from src.preprocessing.transform import transform_df


def run_etl() -> Path:
    raw_path = get_raw_dataset_path()
    df = read_raw_listings(raw_path)
    tdf = transform_df(df)
    out_path = get_processed_dir() / "listings_processed.csv"
    tdf.to_csv(out_path, index=False)
    print(f"Wrote {len(tdf)} rows to {out_path}")
    return out_path


if __name__ == "__main__":
    run_etl()
