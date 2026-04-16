from pathlib import Path

from helper.email_manager import email_handler
from helper.logging_helper import logger
from model.email import success_email, fail_email


def has_files(directory_path: Path) -> bool:
    if not directory_path.exists() or not directory_path.is_dir():
        return False

    return any(item.is_file() for item in directory_path.iterdir())


def process_eams_report_pipeline(output_file_name: str):
    output_dir = Path("output")
    download_file_path = output_dir / output_file_name

    if has_files(output_dir):
        logger.info("file exists")
        email_handler.send_email(success_email)
    else:
        email_handler.send_email(fail_email)
