import requests
from bs4 import BeautifulSoup
import os
import smtplib
from email.mime.text import MIMEText

url = os.getenv('WEBSITE')
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

def get_current_light(soup):
    section = soup.find('section', {'data-id': 'efb6628'}, 'elementor-section')
    if section:
        section_str = str(section)
        if 'rot' in section_str:
            return("rot")
        elif 'grün' in section_str:
            return("grün")
        else:
            return("farblos")

def send_email_notification():
    email_user = os.getenv('EMAIL_USER')
    email_password = os.getenv('EMAIL_PASSWORD')
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    to_email = os.getenv('TO_EMAIL')
    
    msg = MIMEText("Die Ampel ist grün! Call {}".format(os.getenv('PHONE')))
    msg['Subject'] = 'Ampel Checker'
    msg['From'] = email_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(email_user, email_password)
        server.sendmail(email_user, to_email, msg.as_string())

if __name__ == "__main__":
    if get_current_light(soup) == 'grün':
        send_email_notification()
