import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from constants.email_configs import EXTERNAL_EMAIL_HOST, EXTERNAL_EMAIL_PORT, EXTERNAL_EMAIL_ACCOUNT, \
    EXTERNAL_EMAIL_PASSWORD
from helper.logging_helper import logger


class EmailHandler:
    def __init__(self):
        self._log_in_email_account()

    def _log_in_email_account(self):
        logger.info("Logging in email account ...")
        self.server = smtplib.SMTP(
            EXTERNAL_EMAIL_HOST,
            EXTERNAL_EMAIL_PORT)
        self.server.starttls()
        self.server.login(
            EXTERNAL_EMAIL_ACCOUNT,
            EXTERNAL_EMAIL_PASSWORD)

    def send_email(self,
                   to_addr: str,
                   subject: str,
                   message: str
                   ):
        logger.info(f"Preparing to send email f{to_addr=} {subject=} {message=}")
        email = MIMEMultipart()
        email['From'] = EXTERNAL_EMAIL_HOST
        email["To"] = to_addr
        email["Subject"] = subject
        email.attach(MIMEText(message, "html"))
        try:
            logger.info("Sending Email ...")
            self.server.send_message(email)
            self.server.quit()
            logger.info("Email Sent!")
        except Exception as e:
            logger.error(f"Error sending Email {e=}")


email_handler = EmailHandler()
