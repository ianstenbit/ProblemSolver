#!/usr/bin/env python
import imaplib2
from threading import *
import sys
import email
import re
import Text
import Idler
import time
import datetime
import ServerInputManager
import os

M = None
idler = None
thread = None


def check():
	try:
		process_inbox()
	except:
		Text.sendText("Error")

def process_inbox():
	rv, data = M.search(None, "(UNSEEN)")
	if rv != 'OK':
		print "No Messages Found!"
		return

	for num in data[0].split():
		rv, data = M.fetch(num, '(RFC822)')
		if rv != 'OK':
			print "Error getting message ", num
			return
		
		msg = email.message_from_string(data[0][1])
		#print msg['subject']
		#for part in msg.walk():
		#	if part.get_content_type() == 'text/plain':
		#		print re.sub('=.*=', '',  part.get_payload())
		M.store(num, '+FLAGS', '\\Deleted')
		
		msg = msg.as_string()
		
		path = os.path.expanduser("~/Desktop/Scripts/Prefs/comm.txt")	
		file = open(path, 'w')
		
		if not "ianjjohnson" in msg:
			file.write("text")
			msg = msg[msg.index('<td>') + 4 : msg.index('</td>')].strip()
		else:
			file.write("email")
			msg = msg[msg.index('\n\n')::].strip()
		print msg

		file.close()
		
		path = os.path.expanduser("~/Desktop/Scripts/Logs/ServerLog.txt")
		file = open(path, 'a')
		file.write(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
		file.write(":\n")
		file.write(msg)
		file.write("\n")		
		file.close()
		
		print "Logged"
		
		ServerInputManager.respondToMessage(msg)

	M.expunge()
	print "Leaving Box"

# The method that gets called when a new email arrives. 
# Replace it with something better.
def dosync():
	print "Got an event!"
	check()

def idle():
 # Starting an unending loop here
	needsync = True		
	while True:
			
	        # This is part of the trick to make the loop stop 
	        # when the stop() command is given
        	if event.isSet():
           		return
       		 	needsync = False
	        # A callback method that gets called when a new 
	        # email arrives. Very basic, but that's good
		def callback(args):
           		 if not event.isSet():
               			 needsync = True
               			 event.set()
	        # Do the actual idle call. This returns immediately, 
	        # since it's asynchronous.
        	M.idle(callback=callback)
	        # This waits until the event is set. The event is 
	        # set by the callback, when the server 'answers' 
	        # the idle call and the callback function gets 
	        # called.
       		event.wait()
	        # Because the function sets the needsync variable,
	        # this helps escape the loop without doing 
	        # anything if the stop() is called. Kinda neat 
	        # solution.
       		if needsync:
           		event.clear()
            		dosync()


M = imaplib2.IMAP4_SSL('imap.gmail.com')
M.login('ianlinuxserver@gmail.com', 'LinuxMint2015!')
M.select("inbox")
check()

#init
thread = Thread(target=idle)
event = Event()

#start
thread.start()

time.sleep(60*60)

#stop
event.set()

#join
thread.join()

M.expunge()
M.close()
M.logout() 
print "DONE!"


#rv, data = M.select("inbox")
#if rv == 'OK':
#	print "Loading Inbox"
#	process_inbox(M)


