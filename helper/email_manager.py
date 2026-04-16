import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
from typing import List, Optional, Union

from constants.email_configs import (
    EXTERNAL_EMAIL_HOST,
    EXTERNAL_EMAIL_PORT,
    EXTERNAL_EMAIL_ACCOUNT,
    EXTERNAL_EMAIL_PASSWORD
)
from helper.logging_helper import logger
from model.email import Email


class EmailHandler:
    def _attach_files(self,
                      email_msg: MIMEMultipart,
                      file_paths: List[Union[str, Path]]) -> None:
        """
        Private helper method to process and attach files to the MIME message.
        """
        for file_path in file_paths:
            path_obj = Path(file_path)

            if not path_obj.exists() or not path_obj.is_file():
                logger.warning(f"Attachment skipped: File not found at {path_obj}")
                continue

            try:
                with open(path_obj, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                encoders.encode_base64(part)

                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={path_obj.name}"
                )
                email_msg.attach(part)
                logger.info(f"Successfully attached: {path_obj.name}")

            except Exception as e:
                logger.error(f"Failed to attach file {path_obj.name}: {e}")

    def send_email(self,
                   email: Email) -> None:
        to_addr = email.to
        subject = email.subject
        message = email.body
        attachments = email.attachment

        formatted_to = ", ".join(to_addr)
        logger.info(f"Preparing to send email to {formatted_to} | Subject: '{subject}'")

        email_msg = MIMEMultipart()
        email_msg['From'] = EXTERNAL_EMAIL_ACCOUNT
        email_msg["To"] = formatted_to
        email_msg["Subject"] = subject
        email_msg.attach(MIMEText(message, "html"))

        if attachments:
            self._attach_files(email_msg, attachments)

        try:
            logger.info("Connecting to SMTP server...")
            with smtplib.SMTP(EXTERNAL_EMAIL_HOST, EXTERNAL_EMAIL_PORT) as server:
                server.starttls()
                server.login(EXTERNAL_EMAIL_ACCOUNT, EXTERNAL_EMAIL_PASSWORD)
                logger.info("Sending payload...")
                server.send_message(email_msg)
            logger.info("Email sent successfully!")

        except smtplib.SMTPAuthenticationError:
            logger.error("SMTP Authentication failed. Check your email credentials.")
        except Exception as e:
            logger.error(f"An unexpected error occurred while sending the email: {e}", exc_info=True)


email_handler = EmailHandler()
