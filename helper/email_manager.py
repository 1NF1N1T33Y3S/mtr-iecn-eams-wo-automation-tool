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


class EmailHandler:
    """
    Handles the composition and transmission of emails, including attachments.

    Adheres to the Single Responsibility Principle by strictly managing
    email construction and SMTP payload delivery.
    """

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
                # Read file in binary mode
                with open(path_obj, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())

                # Encode payload in base64
                encoders.encode_base64(part)

                # Add header to make it an attachment
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={path_obj.name}"
                )

                email_msg.attach(part)
                logger.info(f"Successfully attached: {path_obj.name}")

            except Exception as e:
                logger.error(f"Failed to attach file {path_obj.name}: {e}")

    def send_email(self,
                   to_addr: str,
                   subject: str,
                   message: str,
                   attachments: Optional[List[Union[str, Path]]] = None) -> None:
        """
        Constructs and sends an email via the configured SMTP server.
        Establishes a fresh connection for each send to prevent timeout closures.
        """
        logger.info(f"Preparing to send email to {to_addr} | Subject: '{subject}'")

        # 1. Construct the Email Wrapper
        email_msg = MIMEMultipart()
        email_msg['From'] = EXTERNAL_EMAIL_ACCOUNT  # FIX: Use Account, not Host
        email_msg["To"] = to_addr
        email_msg["Subject"] = subject
        email_msg.attach(MIMEText(message, "html"))

        # 2. Process Attachments
        if attachments:
            self._attach_files(email_msg, attachments)

        # 3. Transmit using a Context Manager for safe resource handling
        try:
            logger.info("Connecting to SMTP server...")
            # The 'with' block ensures .quit() is automatically called, even if an error occurs
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


# Instantiate the global handler
email_handler = EmailHandler()