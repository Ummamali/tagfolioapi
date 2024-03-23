import re
import jsonschema
import os
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from .database import find_document, add_document_to_collection
from bson import ObjectId
import random


def run_schema(instance, schema):
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        return False


def is_valid_password(password):
    # Check if the password is at least 8 characters long
    if len(password) < 8:
        return False

    # Check if the password contains at least one special character and one number
    if not re.search(r"[!@#$%^&*]", password) or not re.search(r"\d", password):
        return False

    return True


def send_email(receiver_email, subject, message):
    try:
        # Check if message is None or empty
        if not message:
            print("Error! Message is empty.")
            return False

        # Set up the MIME
        sender_email = current_app.config.get("MAIL_EMAIL")
        sender_password = current_app.config.get("MAIL_PASSWORD")

        # Check if sender_email or sender_password is None
        if not sender_email or not sender_password:
            print("Error! Sender email or password not configured.")
            return False

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Attach the message to the MIME message
        msg.attach(MIMEText(message, "plain"))

        # Create SMTP session for sending the email
        server = smtplib.SMTP("smtp-mail.outlook.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
        return True
    except Exception as e:
        print(f"Failed to send email. Error: {e}")
        return False


# Following are the messages written for each email type
message_text = {
    "RESET_PASSWORD": {
        "subject": "Reset Password",
        "message_file": "email_messages/change_password.txt",
    },
    "DELETE_ACCOUNT": {
        "subject": "Delete Account",
        "message_file": "email_messages/delete_account.txt",
    },
}


def send_verification_email(emailType, user_id, route):
    subject = message_text[emailType]["subject"]
    current_directory = os.path.dirname(__file__)
    file_path = os.path.join(current_directory, message_text[emailType]["message_file"])
    print(file_path)
    with open(file_path) as f:
        message = f.read()
    doc = find_document("users", {"_id": ObjectId(user_id)})
    reciever_email = doc["email"]
    code = str(random.randint(100000, 999999))
    # If a verification email is sent already, it will not send another verification code
    if not find_document(
        "verifications", {"email": doc["email"], "route": route}
    ) and send_email(reciever_email, subject, message + code):
        add_document_to_collection(
            "verifications",
            {"email": doc["email"], "code": code, "route": route},
        )
        return True
