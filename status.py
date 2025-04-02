import requests
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urls import urls


# Email credentials
class EmailCredentials:
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password


# Email
class EmailNotifier:
    def __init__(self, credentials, recipient_emails):
        self.credentials = credentials
        self.recipient_emails = recipient_emails

    def send_email(self, subject, message):
        try:
            with smtplib.SMTP(self.credentials.smtp_server, self.credentials.smtp_port) as server:
                server.starttls()
                server.login(self.credentials.sender_email, self.credentials.sender_password)

                for recipient_email in self.recipient_emails:
                    msg = MIMEMultipart()
                    msg['From'] = self.credentials.sender_email
                    msg['To'] = recipient_email
                    msg['Subject'] = subject
                    msg.attach(MIMEText(message, 'plain'))

                    server.sendmail(self.credentials.sender_email, recipient_email, msg.as_string())
                    print(f"Email sent to {recipient_email}")
        except Exception as e:
            
            print(f"Failed to send email: {e}")


# check URLs and return status
class UrlChecker:
    def __init__(self, urls):
        self.urls = urls

    def check_urls(self):
        results = []
        for url in self.urls:
            try:
                response = requests.get(url, timeout=10)
                results.append((url, response.status_code))
            except Exception as e:
                results.append((url, str(e)))
        return results


# Email credentials
def main():
    email_credentials = EmailCredentials(
        smtp_server='smtp.gmail.com',
        smtp_port=587,
        sender_email='keerthi.office1990@gmail.com',
        sender_password = os.environ["APP_PASSWORD"] # App password'

    )
    # recipient_emails = ['ravinda.esol@gmail.com', 'keerthi.office1990@gmail.com']
    recipient_emails = ['ravinda.esol@gmail.com', 'keerthi.office1990@gmail.com']
    email_notifier = EmailNotifier(email_credentials, recipient_emails)

    # Use the outer UrlChecker class (returns all results)
    url_checker = UrlChecker(urls)
    results = url_checker.check_urls()

    failed = [r for r in results if r[1] != 200]
    message_lines = []

    for url, status in results:
        if status == 200:
            message_lines.append(f"✅ {url} is UP (200 OK)")
        else:
            message_lines.append(f"❌ {url} FAILED with status: {status}")

    subject = "✅ All Websites Are Up" if not failed else "❗ Some Websites Failed"
    message = "\n".join(message_lines)

    email_notifier.send_email(subject, message)


# Run the script
if __name__ == "__main__":
    main()
