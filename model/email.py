from dataclasses import dataclass
from typing import List, Optional

from constants.email_configs import RECIPIENTS


@dataclass
class Email:
    to: List[str]
    subject: str
    body: str
    attachment: Optional[List[str]] = None


email_subject = "[Action Required] EAMS CMCR Work Order Summary"
success_body = """
Dear RRU,
    Please assist to fill in the attached Excel for our close out in EAMS.
Best Regards,
IECC
"""
fail_body = """
Dear RRU,
    There are NO open EAMS CMCR Work Order.
    You may ignore this email.
Best Regards,
IECC
"""
success_email = Email(RECIPIENTS, email_subject, success_body)
fail_email = Email(RECIPIENTS, email_subject, fail_body)
