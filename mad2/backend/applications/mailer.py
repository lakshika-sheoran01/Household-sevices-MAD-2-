import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

def send_mail(email, subject, email_content, attachment=None):
    # Define email server and credentials
    smtp_server_host = "localhost"
    smtp_port = 1025
    sender_email = "admin@gs.com"
    sender_password = ""

    # Create the email message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = email
    msg["Subject"] = subject

    # Attach the HTML content to the email
    msg.attach(MIMEText(email_content, "html"))

    # Attach the HTML content to the email
    if attachment:
        with open(attachment, "rb") as attachment_content:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment_content.read())
            encoders.encode_base64(part)
        # part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(attachment))
        print(os.path.basename(attachment))
        part.add_header('Content-Disposition', f'attachment; filename= "{os.path.basename(attachment)}"')
        msg.attach(part)

    # Set up email server
    server = smtplib.SMTP(host=smtp_server_host, port=smtp_port)
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
    print("Mail sent")

