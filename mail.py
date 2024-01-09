import time
import smtplib
from email.mime.text import MIMEText
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Gmail SMTP settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587  # Use 587 for TLS
SMTP_USERNAME = 'webserver193@gmail.com'
SMTP_PASSWORD = 'thic kkly zstm dtwn'  # Use an App Password for security

EMAIL_FROM = 'webserver193@gmail.com'
EMAIL_TO = 'mason.rauschkolb@gmail.com'

# Function to send an email
def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Event handler to monitor file changes
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith('.txt'):
            print(f"File '{event.src_path}' has been updated.")
            with open(event.src_path, 'r') as file:
                file_content = file.read()
                send_email(f"New Message from Contact Form", file_content)

if __name__ == "__main__":
    # Specify the directory and file to monitor
    path_to_monitor = '/home/raspberry/Desktop/Portfolio Site/'  # Change this to the directory containing the text file
    file_to_monitor = 'messages.txt'  # Change this to the name of your text file

    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_monitor, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
