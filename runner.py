import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
import time

# Disable SSL verification
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# URL to monitor
url = 'https://www.signupgenius.com/go/10C0C4FAEA82FABFEC34-dining1/#/'

# Email configuration
sender_email = "your_email@gmail.com"
sender_password = "your_app_password"
recipient_email = "recipient@example.com"
smtp_server = "smtp.gmail.com"
smtp_port = 587

def check_for_new_slots():
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all signup buttons
    signup_buttons = soup.find_all('button', class_='SUGbutton')
    
    # Check if any button's text is not "Full" or "full"
    available_slots = [button for button in signup_buttons if 'full' not in button.text.lower()]
    
    return len(available_slots)

def send_email(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

def main():
    previous_slot_count = 0
    
    while True:
        current_slot_count = check_for_new_slots()
        
        if current_slot_count > previous_slot_count:
            new_slots = current_slot_count - previous_slot_count
            subject = "New Slots Available!"
            body = f"{new_slots} new slot(s) have been released on SignUpGenius. Check the page: {url}"
            send_email(subject, body)
            print(f"Email sent: {new_slots} new slot(s) available")
        
        previous_slot_count = current_slot_count
        print(f"Current available slots: {current_slot_count}")
        time.sleep(300)  # Check every 5 minutes

if __name__ == "__main__":
    main()
