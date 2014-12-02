#################################
# "Language Journal" By: Ida Chow
#################################

# switch to JSON, CSV ???!!!

# languagejournal_main:
# main file for languagejournal

from Tkinter import *
import random
import copy
import time
import csv
import winsound
import pyaudio
import sys
from eventBasedAnimationClass import EventBasedAnimationClass

### import other class files
from vocab import Vocab
from window import Window

## det window size
import ctypes
user32 = ctypes.windll.user32
screensize = screenWidth, screenHeight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
print screensize



class LanguageJournal(EventBasedAnimationClass):
	def __init__(self,width,height):

		self.timerDelay = None # in milliseconds (set to None to turn off timer)

		self.width = width
		self.height = height
		self.cx = width/2
		self.cy = height/2
		self.currentWindow = 0


	def Enter(self,event):
		""" Someone Pressed Enter """
		print "You entered >> %s" % (self.entrybox.get())
	
	def onMouseMotion(self, event):
		pass

	def onKeyPressed(self, event):
		if (event.char == "!"): 
			filename = "data.csv"
			# opening the file with w+ mode truncates the file
			f = open(filename, "w+")
			f.close()

	def onMousePressed(self,event):
		x,y = event.x_root, event.y_root
		print x,y
		backcoord = self.height/20
		if self.currentWindow == 0:
			if (self.cx+10 <= x <= self.cx+110) and (self.cy-50 <= y <= self.cx+50):
				self.currentWindow = 1
				self.window.screen_newVocab() 
				# winsound.Beep(3000, 1000)
			elif (self.cx-110 <= x <= self.cx-10) and (self.cy-50 <= y <= self.cx+50):
				self.currentWindow = 2
				self.window.screen_viewVocab()
		if self.currentWindow == 1 or self.currentWindow == 2:
			# select cell of listbox for CSV file
			if (backcoord <= x <= backcoord+100) and (backcoord <= y <= backcoord+100):
				if self.currentWindow == 1:
					self.window.frame_entryvocab.destroy()
					self.window.frame_entrydefinition.destroy()
					self.window.frame_entrysave.destroy()
					self.window.frame_audiosave.destroy()
					self.window.frame_audioplay.destroy()
				if self.currentWindow == 2:
					if self.window.lb.curselection() != ():
						self.window.b5.destroy()
						self.window.frame_displayaudioplay.destroy()
					self.window.myframe.destroy()
					self.window.canvasScroller.destroy()
				self.currentWindow = 0
			elif self.currentWindow == 2 and self.window.lb.curselection() != ():
				self.window.screen_viewVocab_displayVocab()

	def redrawAll(self):
		if self.currentWindow == 0:
			width = self.width
			height = self.height
			self.canvas.create_rectangle(0,0,width,height,fill="#2D2E27")
			self.selectCurrentWindow()



	def selectCurrentWindow(self):
		if (self.currentWindow == 0):
			self.window.screen_start()
		elif (self.currentWindow == 1):
			self.window.screen_newVocab()
		else: pass

	def initAnimation(self):

		self.canvas.bind("<Button-1>", lambda event: self.onMousePressed(event))
		self.window = Window(self.canvas,self.width, self.height,self.cx,self.cy,self.root)

		self.redrawAll()



myapp = LanguageJournal(1*screenWidth,.95*screenHeight)

myapp.run()



############ mp3 testing 

# import winsound

# winsound.Beep(3000, 1000)
# winsound.PlaySound('ocean_nobirds.mp3', winsound.SND_FILENAME)