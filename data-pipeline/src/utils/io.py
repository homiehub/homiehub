from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def get_data_dir() -> Path:
    return get_project_root() / "data"


def get_raw_dir() -> Path:
    return get_data_dir() / "raw"


def get_processed_dir() -> Path:
    d = get_data_dir() / "processed"
    d.mkdir(parents=True, exist_ok=True)
    return d


def get_raw_dataset_path() -> Path:
    return get_raw_dir() / "structured_listings_nlp.csv"
