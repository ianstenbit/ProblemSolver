#!/usr/bin/env python
import re
import sys
import Text
import re
from yahoo_finance import Share

args = sys.argv

def respondToStockStatement(statement):

	def addTicker(tck):
		prefsFile = open("Prefs/tickers.txt", 'a+')
			
		print tck
		if not tck + "\n" in prefsFile.readlines():
			if Share(tck).get_price() != None:
				prefsFile.write(tck + "\n")
				Text.sendText("Ticker " + tck + " added to database.")
			else:
				Text.sendText("Invalid ticker " + tck)
		else: 
			Text.sendText("Ticker " + tck + " already in system")

		prefsFile.close()
	
	print "Stock Statement: " + statement
	
	if "add" in statement or "put" in statement or "start" in statement:
		
		print "adding"		
		
		tickers = re.findall(r"'.{1,4}'", statement)
		
		for tick in tickers:
			addTicker(tick[1:-1].upper())

	elif "log" in statement or "file" in statement or "data" in statement:
		
		tickers = re.findall(r"'.{1,4}'", statement)
				
		for tick in tickers:
			t = tick[1:-1].upper()
			print "log for " + t
			Text.sendWithAttachment("Data for " + t, "Data/" + t + "_Data.txt")		

			
def respondToStockQuestion(question):
	print "Responding Stock " + question 
	tickers = re.findall(r"'.{1,4}'", question)
	print tickers
	msg = ""
	for tick in tickers:
		t = tick[1:-1].upper()
		print t
		share = Share(t)
		msg += t + " price is "+share.get_price() + "\n"
	Text.sendText(msg[:-1])

def respondToStatement(statement):
	print "STATEMENT: ", statement
	if "stock" in statement:
		respondToStockStatement(statement)

def respondToQuestion(question):
	print "QUESTION: ", question
	if "stock" in question:
		respondToStockQuestion(question)

def respondToMessage(message):
	messages = [m.strip().lower() for m in message.split("\n")]
	for m in messages:
		if "?" in m:
			respondToQuestion(m)
		elif  m !=  "":
			respondToStatement(m)

if len(args) > 1:
	for arg in args[1:]:
		respondToMessage(arg)
