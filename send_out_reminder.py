from pathlib import Path

from constants.file_paths import archive_directory, ARCHIVE_DIR_PATH, OUTPUT_DIR_PATH
from utils.download_report_pipeline import download_report_pipeline, move_to_archive
from utils.process_report_pipeline import email_based_on_eams_report
from utils.utils import generate_timestamped_filename


def main():
    output_file_name = generate_timestamped_filename()
    output_file_path = OUTPUT_DIR_PATH / output_file_name

    records = download_report_pipeline(output_file_name)
    email_based_on_eams_report(output_file_name, records)
    move_to_archive(output_file_path, ARCHIVE_DIR_PATH)


if __name__ == "__main__":
    main()
