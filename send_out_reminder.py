from pathlib import Path

from utils.download_report_pipeline import download_report_pipeline, move_to_archive
from utils.process_report_pipeline import email_based_on_eams_report
from utils.utils import generate_timestamped_filename


def main():
    output_file_name = generate_timestamped_filename()
    output_dir = Path("output")
    output_file_path = output_dir / output_file_name
    housekeeping_dir = Path("archive/")
    records = download_report_pipeline(output_file_name)
    email_based_on_eams_report(output_file_name, records)
    move_to_archive(output_file_path, housekeeping_dir)


if __name__ == "__main__":
    main()
