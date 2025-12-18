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
