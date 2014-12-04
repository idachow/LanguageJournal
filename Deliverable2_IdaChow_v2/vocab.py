
###########################################
# vocab.py class for languagejournal_main.py
###########################################

from Tkinter import *
import random
import copy
import time
import csv
from eventBasedAnimationClass import EventBasedAnimationClass

class Vocab(object):
	def __init__(self,word,definition,date):
		self.word = word
		self.definition = definition
		self.date = date

	def __str__(self):
		return str(self.word) + ": " + str(self.definition) + ": " + str(self.date)

	def saveAll(self):
		c = csv.writer(open("data.csv", "a"))
		c.writerow([self.date,self.word,self.definition])

	def checkAndWrite(self,f,item):
		# checks file to see if existing vocabularly already exists
		# if not, writes it to the file
		self.exist = False
		for line in f:
			if line == item + "\n":
				self.exist = True
		if self.exist == False:
			f.write(item)