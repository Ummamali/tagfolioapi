import re
import jsonschema
import os
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



def run_schema(instance, schema):
    try:
        jsonschema.validate(instance=instance, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError as e:
        return False


def send_email(receiver_email, subject, message):
    try:
        # Set up the MIME
        sender_email = current_app.config['MAIL_EMAIL']
        sender_password = current_app.config['MAIL_PASSWORD']
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Attach the message to the MIME message
        msg.attach(MIMEText(message, 'plain'))

        # Create SMTP session for sending the email
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")