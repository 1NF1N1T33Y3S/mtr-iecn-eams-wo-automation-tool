from enum import Enum


class EAMSStatus(Enum):
    # APPR = "Approved" -> open
    # VOID = "Void" -> completed
    # CANCEL_CLOSE = "Cancel Closed" -> open
    # CLOSE = "Closed" -> completed
    # REFER_CLOSE = "Refer Closed" -> completed
    # CANCEL = "Cancel" -> completed
    # COMP = "Completed" -> completed
    # REFER = "Referred" -> open
    # INPRG = "In Progress" -> open
    # WAPPR = "Waiting on Approval" -> open
    # WSCH = "Waiting to be Scheduled" -> open
    COMPLETED = "completed"
    OPENED = "open"
    MISSING = "Missing Record in EAMS"
