from pathlib import Path
from typing import List

from constants.file_paths import INPUT_DIR_PATH
from model.eams_wo import EAMSWorkOrder
from utils.download_report_pipeline import download_report_pipeline, move_to_archive, clear_folder
from utils.process_report_pipeline import email_based_on_eams_report
from utils.close_out_wo_pipeline import read_excel_report, close_eams_wos
from utils.utils import generate_timestamped_filename
from utils.work_order_mapper import map_dataframe_to_work_orders


def main():
    # TODO run code to put the unprocessed xlsx file into 1.to_process

    input_file = "result_2026_04_22_103351.xlsx"
    input_file_path = INPUT_DIR_PATH / input_file
    df = read_excel_report(str(input_file_path))
    records: List[EAMSWorkOrder] = map_dataframe_to_work_orders(df)
    close_eams_wos(records)


if __name__ == '__main__':
    main()
