from pathlib import Path
from typing import List

from constants.email_configs import RECIPIENTS, EMAIL_SUBJECT
from helper.email_manager import email_handler
from helper.logging_helper import logger
from model.eams_wo import EAMSWorkOrder
from model.email import get_report_attached_email, get_no_work_order_email, Email


def has_files(directory_path: Path) -> bool:
    if not directory_path.exists() or not directory_path.is_dir():
        return False

    return any(item.is_file() for item in directory_path.iterdir())


def process_eams_report_pipeline(
        output_file_name: str,
        records: List[EAMSWorkOrder]):
    output_dir = Path("output")
    output_file_path = output_dir / output_file_name
    attachments = [str(output_file_path)]

    if has_files(output_dir):
        logger.info("file exists")
        success_body = get_report_attached_email(len(records))
        success_email = Email(RECIPIENTS, EMAIL_SUBJECT, success_body, attachments)
        email_handler.send_email(success_email)
    else:
        fail_body = get_no_work_order_email()
        fail_email = Email(RECIPIENTS, EMAIL_SUBJECT, fail_body)
        email_handler.send_email(fail_email)
