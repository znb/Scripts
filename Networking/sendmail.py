#!/usr/bin/python
# Simple script to send out email

import smtplib
from email.mime.text import MIMEText

me = "matt@example.com"
you = "matt@ilovechaosmonkey.com"

msg = MIMEText("This is a test body")
msg['Subject'] = "This is a subject line"
msg['From'] = me
msg['To'] = you


s = smtplib.SMTP("there.must.be.a.better.way.com")
s.sendmail(me, [you], msg.as_string())
s.quit()
