from dataclasses import dataclass
from typing import List, Optional



@dataclass
class Email:
    to: List[str]
    subject: str
    body: str
    attachment: Optional[List[str]] = None


def get_no_work_order_email() -> str:
    """
    Returns the HTML formatted email body for the 'No Work Order' notification.

    Uses standard HTML tags:
    - <p> for paragraphs
    - <br> for line breaks
    - CSS 'margin-left' for the indentation you requested
    """
    return """
    <html>
        <body style="font-family: Arial, sans-serif; color: #333333;">
            <p>Dear Duty E-shift Supervisor/ Technical Officer,</p>
            <p style="margin-left: 40px; color: #0055A4;">
                There are <strong>NO</strong> open EAMS CMCR Work Orders.<br>
                You may ignore this email.
            </p>
            <p>
                Best Regards,<br>
                <strong>IECC</strong>
            </p>
        </body>
    </html>
    """


def get_report_attached_email(record_count: int) -> str:
    """
    Example of a dynamic template using f-strings to inject variables.
    """
    return f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <p>Dear Duty E-shift Supervisor/ Technical Officer,</p>
            <p>Please fill in the details of the work orders you have completed and return the Daily Outstanding job reminder to IECC on or before 14:00.</p>
            <p>Total records to close: <strong>{record_count}</strong></p>
            <p>Best Regards,<br>IECC</p>
        </body>
    </html>
    """



