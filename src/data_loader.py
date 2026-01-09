import os
import logging
import pandas as pd
import numpy as np
import kaggle
from zipfile import ZipFile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Config
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "creditcard.csv")
PARQUET_PATH = os.path.join(DATA_DIR, "creditcard.parquet")
DATASET_NAME = "mlg-ulb/creditcardfraud"

def data_loader():
    """
    Download data from Kaggle and convert to Parquet
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if os.path.exists(PARQUET_PATH):
        logger.info(f"File found at {PARQUET_PATH}. Skip download")
        return
    
    if not os.path.exists(CSV_PATH):
        logger.info(f"Downloading {DATASET_NAME} from Kaggle...")
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(DATASET_NAME, path=DATA_DIR, unzip=True)
        logger.info("Download complete.")
    
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.lower() for c in df.columns]
    df.to_parquet(PARQUET_PATH, index=False)
    logger.info(f"File saved to {PARQUET_PATH}")

def load_data() -> pd.DataFrame:
    if not os.path.exists(PARQUET_PATH):
        data_loader()
    
    logger.info(f"Loading data from {PARQUET_PATH}...")
    df = pd.read_parquet(PARQUET_PATH)
    return df

if __name__ == "__main__":
    data_loader()
    df = load_data()
    