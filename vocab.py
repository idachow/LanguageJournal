
###########################################
# vocab.py class for languagejournal_main.py
###########################################

from Tkinter import *
import random
import copy
import time
import csv
import winsound
import pyaudio
import sys
import os
from eventBasedAnimationClass import EventBasedAnimationClass


## det window size
import ctypes
user32 = ctypes.windll.user32
screensize = screenWidth, screenHeight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

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

	def editWord(self,entry,indexOfEdit,date,definition,originalName):

		#pulling in originalName only for .wav file rewrite purposes
		
		def editVocab():
			vocab_list = []

			# Read all data from the csv file.
			with open('data.csv', 'rb') as b:
				vocab = csv.reader(b)
				vocab_list.extend(vocab)

			# data to override in the format {line_num_to_override:data_to_write}. 
			line_to_override = {indexOfEdit:[date, entry, definition] }

			# Write data to the csv file and replace the lines in the line_to_override dict.
			with open('data.csv', 'wb') as b:
				writer = csv.writer(b)
				for line, row in enumerate(vocab_list):
					 data = line_to_override.get(line, row)
					 writer.writerow(data)

			return

		editVocab()

		# replacement of audio so that the .wav 
		# file still hooks up to the same place
		src ="audio/"+originalName+".wav"
		dst = "audio/"+entry+".wav"
		os.rename(src,dst)


	def editDef(self,entry,indexOfEdit,date,name):

		def editVocab():
			vocab_list = []

			# Read all data from the csv file.
			with open('data.csv', 'rb') as b:
				vocab = csv.reader(b)
				vocab_list.extend(vocab)

			# data to override in the format {line_num_to_override:data_to_write}. 
			line_to_override = {indexOfEdit:[date, name, entry] }

			# Write data to the csv file and replace the lines in the line_to_override dict.
			with open('data.csv', 'wb') as b:
				writer = csv.writer(b)
				for line, row in enumerate(vocab_list):
					 data = line_to_override.get(line, row)
					 writer.writerow(data)

			return

		editVocab()