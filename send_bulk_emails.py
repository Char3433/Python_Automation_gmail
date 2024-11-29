import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import time

# Set your email and app password here
SENDER_EMAIL = "FFEFFE@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "o00000b"  # Your generated App Password (no spaces)

# Files to use
RECIPIENTS_FILE = "recipients.txt"
EMAIL_BODY_FILE = "email_body.txt"
ATTACHMENT_FILE = "resume.pdf"

def send_email(recipient, subject, body, attachment_path=None):
    """Send an email to a single recipient."""
    try:
        # Gmail SMTP server details
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        # Create email
        message = MIMEMultipart()
        message["From"] = SENDER_EMAIL
        message["To"] = recipient
        message["Subject"] = subject

        # Attach email body
        message.attach(MIMEText(body, "plain"))

        # Attach file if provided
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename={os.path.basename(attachment_path)}",
                )
                message.attach(part)

        # Connect to SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)  # Enables debug output for troubleshooting
            server.starttls()  # Start TLS encryption
            server.login(SENDER_EMAIL, SENDER_PASSWORD)  # Login with App Password
            server.sendmail(SENDER_EMAIL, recipient, message.as_string())  # Send email
            print(f"Email successfully sent to {recipient}!")

    except smtplib.SMTPAuthenticationError:
        print(f"Authentication failed for {SENDER_EMAIL}. Check your email/password.")
    except Exception as e:
        print(f"Failed to send email to {recipient}. Error: {e}")


if __name__ == "__main__":
    try:
        # Read recipients from file
        with open(RECIPIENTS_FILE, "r") as file:
            recipients = [line.strip() for line in file if line.strip()]

        # Read email body from file
        with open(EMAIL_BODY_FILE, "r") as file:
            email_body = file.read()

        # Email subject
        subject = "Application for DevOps Engineer Role"

        # Send emails with retry logic
        for recipient in recipients:
            try:
                send_email(recipient, subject, email_body, ATTACHMENT_FILE)
            except Exception as e:
                print(f"Retrying {recipient} in 5 seconds...")
                time.sleep(5)  # Wait 5 seconds before retrying
                try:
                    send_email(recipient, subject, email_body, ATTACHMENT_FILE)
                except Exception as retry_error:
                    print(f"Failed again for {recipient}. Error: {retry_error}")

    except FileNotFoundError as fnf_error:
        print(f"File not found: {fnf_error}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
