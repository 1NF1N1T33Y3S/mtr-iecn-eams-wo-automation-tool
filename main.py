from pathlib import Path

from utils.download_report_pipeline import download_report_pipeline, move_to_archive, clear_folder
from utils.process_report_pipeline import email_based_on_eams_report
from utils.close_out_wo_pipeline import read_excel_report, close_single_wo
from utils.utils import generate_timestamped_filename
from utils.work_order_mapper import map_dataframe_to_work_orders



def main():
    input_report_dir = Path("to_process")
    input_file = "result_2026_04_22_103351.xlsx"
    input_file_path = input_report_dir / input_file
    df = read_excel_report(str(input_file_path))
    records = map_dataframe_to_work_orders(df)
    for r in records:
        close_single_wo(r)


if __name__ == '__main__':
    main()
