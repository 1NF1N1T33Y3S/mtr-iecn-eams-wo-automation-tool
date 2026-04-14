import os, time
from pathlib import Path
from datetime import datetime
from typing import List

from constants.constants import default_download_path
from constants.file_paths import iecc_centralized_log_file_path
from helper.chrome_helper import ChromeHelper
from helper.crawler_helper import CrawlerHelper, crawler_helper
from helper.data_helper import DataHelper, parse_work_order, filter_df, get_fault_cleared_df, filter_nan_df, \
    get_eams_incomplete_df, data_helper
from helper.excel_helper import ExcelHelper, excel_helper
from helper.logging_helper import logger
from model.work_order import WorkOrder


def output_result_to_excel(excel: ExcelHelper, wos: List[WorkOrder]):
    for w in wos:
        logger.info(f"{w.id=} {w.wo_id=} {w.actual_start_date=} {w.actual_finish_date=}")
        r = excel.get_row_by_column(0, w.id)
        excel.write("EAMS WO Completed", r, w.job_status)
        excel.write("EAMS WO Failure Message", r, w.execution_error_message)


def main():
    logger.info('CMCR Automation Tool')
    logger.info("Downloading today's CM/PM Report for LAR")
    # (
    #     crawler_helper
    #     .set_chrome_helper(ChromeHelper())
    #     .login()
    #     .go_to_wo_tracking_page()
    #     .search_and_download_reports()
    # )

    logger.info("Renaming the downloaded report")
    downloads_path = Path.home() / default_download_path
    files = list(downloads_path.glob("*.xls"))
    if not files:
        logger.warning("No Excel files found in the Downloads folder.")
    else:
        latest_file = max(files, key=lambda p: p.stat().st_mtime)
        current_time = datetime.now().strftime("%Y_%m_%d_%H%M%S")
        new_filename = f"{current_time}.xls"
        new_file_path = downloads_path / new_filename
        try:
            latest_file.rename(new_file_path)
            logger.info(f"Renamed: {latest_file.name}")
            logger.info(f"To:      {new_filename}")
        except FileExistsError:
            logger.error(f"Error: A file named {new_filename} already exists.")


if __name__ == '__main__':
    main()
