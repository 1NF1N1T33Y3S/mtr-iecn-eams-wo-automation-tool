from pathlib import Path
from typing import Union, Dict
import pandas as pd

from helper.chrome_helper import ChromeHelper
from helper.crawler_helper import crawler_helper
from helper.logging_helper import logger
from model.eams_wo import EAMSWorkOrder


def read_excel_report(file_path: Union[str, Path],
                      sheet_name: str = "Sheet9") -> pd.DataFrame:
    path_obj = Path(file_path)

    if not path_obj.exists():
        logger.error(f"File not found: {path_obj}")
        raise FileNotFoundError(f"Cannot locate the Excel file at {path_obj}")

    try:
        logger.info(f"Reading sheet '{sheet_name}' from {path_obj.name}...")
        df = pd.read_excel(path_obj, sheet_name=sheet_name, header=0)
        logger.info(f"Successfully loaded {len(df)} records from '{sheet_name}'.")
        return df

    except ValueError as ve:
        logger.error(f"Sheet '{sheet_name}' does not exist in the workbook: {ve}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"An unexpected error occurred while reading the Excel file: {e}", exc_info=True)
        return pd.DataFrame()


def read_all_excel_sheets(file_path: Union[str, Path]) -> Dict[str, pd.DataFrame]:
    path_obj = Path(file_path)

    if not path_obj.exists():
        raise FileNotFoundError(f"Cannot locate the Excel file at {path_obj}")

    try:
        logger.info(f"Loading entire workbook: {path_obj.name}...")
        all_sheets = pd.read_excel(path_obj, sheet_name=None)
        logger.info(f"Successfully loaded {len(all_sheets)} sheets.")
        return all_sheets

    except Exception as e:
        logger.error(f"Failed to load workbook: {e}")
        return {}


def close_single_wo(r: EAMSWorkOrder):
    (
        crawler_helper
        .set_chrome_helper(ChromeHelper())
        .login()
        .go_to_wo_tracking_page()
        .close_single_wo(r)
    )
