#!/usr/bin/python

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mechanicalsoup
import lxml


def send_email(current_status):

    credentials = []

    with open("blake_personal_info.txt", "r") as file:

        for line in file:
            credentials.append(line.split(":")[1].strip())

    smtp = credentials[0]
    email = credentials[1]
    password = credentials[2]

    try:
        s = smtplib.SMTP(smtp)
        s.starttls()
        s.login(email, password)
    except smtplib.SMTPAuthenticationError:
        print('Failed to login')
    else:
        print('Logged in! Composing message..')
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Tesla Status Update"
        msg['From'] = email
        msg['To'] = email

        msgText = "We have detected that the status of your Tesla has updated to: " + current_status

        part = MIMEText(msgText, 'plain')
        msg.attach(part)
        s.sendmail(email, email, msg.as_string())
        s.quit()
        print('Message has been sent.')


def main():

    url = "https://www.tesla.com/teslaaccount/profile?rn=RN109198377"

    browser = mechanicalsoup.StatefulBrowser(
        soup_config={'features': 'lxml'},
        raise_on_404=True,
        user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    )
    browser.open(url)

    login_form = browser.select_form()

    login_form.set("email", "blakecschmidt@gmail.com")
    login_form.set("password", "Blakes3425!")
    browser.submit_selected()

    page = browser.get_current_page()

    status_div = page.find_all(id="section-hero")[1]
    current_status = status_div.find_next("h2").contents[0]

    send_email("oiii")

    if current_status != "Prepare for delivery":
        send_email(current_status)

    browser.close()


main()
