import datetime
from utils.download_report_pipeline import download_report, download_report_pipeline
from utils.process_report_pipeline import process_eams_report_pipeline
from utils.utils import generate_timestamped_filename


def main():
    output_file_name = generate_timestamped_filename()
    download_report_pipeline(output_file_name)
    process_eams_report_pipeline(output_file_name)


if __name__ == '__main__':
    main()
