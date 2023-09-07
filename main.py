#!/usr/bin/python3

import smtplib
import inspect
from uuid import uuid4
import os

def send_email(email_host, email_port, user, password, email_from, email_to, email_body, email_subject):
    email_port = int(email_port)
    _user, email_domain = email_from.split('@', 1)
    email_text = inspect.cleandoc(f"""\
    Message-ID: <{uuid4()}@{email_domain}>
    From: Python SMTP Sender <%s>
    To: %s
    Subject: %s

    %s
    """) % (email_from, email_to, email_subject, email_body)
    try:
        smtp = smtplib.SMTP_SSL if email_port == 465 else smtplib.SMTP
        smtp_server = smtp(email_host, email_port)
        smtp_server.ehlo()

        if email_port == 465:
            smtp_server.login(user, password)

        smtp_server.sendmail(email_from, email_to, email_text.encode('UTF-8'))
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)
    return


def main():
    with open('/var/lib/badtrack/secrets.env','r') as f:
        text = f.read()
        entries = text.split('\n')
        email_user = entries[0].split(' = ')[1]
        email_password = entries[1].split(' = ')[1]

    email_host = 'relay.mailbaby.net'
    email_port = '465'
    user = email_user
    password = email_password
    email_from = 'sender@obsi.com.au'
    email_to = 'robinchew@gmail.com'
    send_email(email_host,email_port,user,password,email_from,email_to,'Hello','Cron example email')
    return


if __name__ == '__main__':
    main()