#!/usr/bin/env python

import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

sender = "ianlinuxserver@gmail.com"
recipients = ["3038153710@mms.att.net", "ianjjohnson@icloud.com"]

subject = "Message from your Linux server"

def build(s, b):
	return """\
	From: %s
	To: %s
	Subject: %s
	\n
	%s
	""" % (sender, ", ".join(recipients), s, b)

def sendText(text):

	body = text + ""
	
	path = os.path.expanduser("~/Desktop/Scripts/Prefs/comm.txt")
	file = open(path, 'r')

	message = build(subject, body)

	servr = smtplib.SMTP("smtp.gmail.com:587")
	servr.starttls()
	servr.login(sender, "LinuxMint2015!")

	if "text" in file.read():
		servr.sendmail(sender, recipients[:1], body)
	else:
		servr.sendmail(sender, recipients[1:], message)

	servr.quit()

	print "Sent Text: " + body

def sendWithAttachment(text, path):
	
	print path
	
	msg = MIMEMultipart()
	msg["Subject"] = text
	msg.preamble = "Stock Data"
	
	p = os.path.expanduser("~/Desktop/Scripts/Prefs/comm.txt")
	prefs = open(p, 'r')	
	
	file = open(path, "r+")
	att = MIMEText(file.read())
	msg.attach(att)

	servr = smtplib.SMTP("smtp.gmail.com:587")
	servr.starttls()
	servr.login(sender, "LinuxMint2015!")
	
	if "text" in prefs.read():
		servr.sendmail(sender, recipients[:1], msg.as_string())
	else:
		servr.sendmail(sender, recipients[1:], msg.as_string())

	servr.quit()
#sendText('Text being sent')

