import datetime
from typing import List

from enums.eams_status import EAMSStatus


def map_eams_status(values: List[str]) -> EAMSStatus:
    if (
            "APPR" in values or
            "CANCEL_CLOSE" in values or
            "REFER" in values or
            "INPRG" in values or
            "WAPPR" in values or
            "WSCH" in values):
        return EAMSStatus.OPENED
    if (
            "VOID" in values or
            "CLOSE" in values or
            "REFER_CLOSE" in values or
            "CANCEL" in values or
            "COMP" in values):
        return EAMSStatus.COMPLETED
    return EAMSStatus.MISSING


def map_to_eams_status(status: str) -> EAMSStatus:
    if status in ["COMP"]:
        return EAMSStatus.COMPLETED
    if status in ["OPEN"]:
        return EAMSStatus.OPENED
    return EAMSStatus.MISSING


def check_records_in_eams():
    pass


def generate_timestamped_filename(prefix: str = "result",
                                  extension: str = ".xls") -> str:
    """Generates a dynamically named file string with a current timestamp."""
    if not extension.startswith('.'):
        extension = f".{extension}"
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
    return f"{prefix}_{current_time}{extension}"
