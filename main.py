from utils.download_report_pipeline import download_report_pipeline
from utils.process_report_pipeline import process_eams_report_pipeline
from utils.utils import generate_timestamped_filename


def main():
    output_file_name = generate_timestamped_filename()
    records = download_report_pipeline(output_file_name)
    process_eams_report_pipeline(output_file_name, records)

    # for debug only
    # process_eams_report_pipeline("final_report.xlsx", [])

    # input_report_dir = Path("to_process")
    # input_file = "final_report.xlsx"
    # input_file_path = input_report_dir / input_file
    # read_excel_report(str(input_file_path))


if __name__ == '__main__':
    main()
