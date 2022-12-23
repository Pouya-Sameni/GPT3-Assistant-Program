import email
import smtplib
import ssl
from sms_mms_providers import PROVIDERS
from decouple import config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import imaplib
import time
import xml.etree.ElementTree as ET
import parsers

def send_sms_via_email(
    number: str,
    message: str,
    subject: str = "",
    smtp_server: str = "smtp.gmail.com",
    smtp_port: int = 465,
    provider="Telus"
):

    sender_credentials = (config('emailUser'), config('emailPass'))

    sender_email, email_password = sender_credentials

    receiver_email = f'{number}@{PROVIDERS.get(provider).get("sms")}'
    
    email_message = f"Subject:{subject}\nTo:{receiver_email}\n{message}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    #msg['Message'] = message
    msg.attach(MIMEText(message))
    with smtplib.SMTP_SSL(
        smtp_server, smtp_port, context=ssl.create_default_context()
    ) as email:
        email.login(sender_email, email_password)
        email.sendmail(msg['From'], msg['To'], msg.as_string())

def recieve_sms_via_email():
    # Connect to the IMAP server
    imap_server = imaplib.IMAP4_SSL('imap.gmail.com')

    # Login to the account
    imap_server.login(config('emailUser'), config('emailPass'))

    # Select the mailbox you want to check for new messages
    imap_server.select('INBOX')
    result, data = imap_server.search(None, 'UNSEEN')
    if result == 'OK':
        # If there are new messages, get the IDs of the messages
        msg_ids = data[0]
        msg_id_list = msg_ids.split()
        if len(msg_id_list) > 0:
            # Get the latest message
            latest_msg_id = msg_id_list[-1]
            result, data = imap_server.fetch(latest_msg_id, "(RFC822)")
            if result == 'OK':
                # Parse the message using the email library
                msg = email.message_from_bytes(data[0][1])

                # Get the message body
                if msg.is_multipart():
                    # If the message is multipart, get the plain text version of the message
                    msg_body = msg.get_payload(0).get_payload(decode=True)
                else:
                    # If the message is not multipart, get the message body directly
                    msg_body = msg.get_payload(decode=True)

                # Print the message body
                message = msg_body.decode()
                parsers.get_text_body(message)
                
                return [message,msg['From']]

    # Close the connection to the server
    imap_server.close()
    imap_server.logout()

    return ["",""]
    





