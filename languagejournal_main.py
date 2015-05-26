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

## det window size since this is a full screen app
import ctypes
user32 = ctypes.windll.user32
screensize = screenWidth, screenHeight = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)



class LanguageJournal(EventBasedAnimationClass):
	def __init__(self,width,height):

		self.timerDelay = None # in milliseconds (set to None to turn off timer)

		self.width = width
		self.height = height
		self.cx = width/2
		self.cy = height/2
		self.currentWindow = 0

		self.mouse = 0


	def Enter(self,event):
		pass

	def onMouseMotion(self, event):
		pass

	def onKeyPressed(self, event):
		pass
		# debugging to clear csv
		# if (event.char == "!"): 
			# filename = "data.csv"
			# # opening the file with w+ mode truncates the file
			#f = open(filename, "w+")
			# f.close()

	def onMousePressed(self,event):

		x,y = event.x_root, event.y_root
		cx, cy = self.cx, self.cy
		height,width = self.height,self.width

		# setting proportionate coordinate for back button
		backcoord = self.height/20

		if self.currentWindow == 0:
			# HOME SCREEN OPTIONS
			if (self.cx+10 <= x <= self.cx+110) and (self.cy-50 <= y <= self.cx+50):
				# CLICKED ON: ADD NEW VOCAB SCREEN
				self.currentWindow = 1
				self.window.screen_newVocab() 

			elif (self.cx-110 <= x <= self.cx-10) and (self.cy-50 <= y <= self.cx+50):
				# CLICKED ON: VIEW ALL VOCAB
				self.currentWindow = 2
				self.window.screen_viewVocab()

		elif (backcoord <= x <= backcoord+100) and (backcoord <= y <= backcoord+100):
			# BACK BUTTON OPTIONS (WHEN ON DIFFERENT WINDOWS)
			if self.currentWindow == 1:
				# IF ON ADD VOCAB PAGE, simply destroy all buttons
				self.window.frame_entryvocab.destroy()
				self.window.frame_entrydefinition.destroy()
				self.window.frame_entrysave.destroy()
				self.window.frame_audiosave.destroy()
				self.window.frame_audioplay.destroy()
				self.currentWindow = 0
			elif self.currentWindow == 2:
				# IF ON VIEW ALL PAGE, check different parameters
				# if self.window.lb.curselection() != ():
				# self.window.b5.destroy()
				if self.window.displayEditScreen == True:
					# if edit screen is open, destroy all edit frames
					self.window.frame_editTermSave.destroy()
					self.window.frame_editTerm.destroy()
					self.window.frame_editDefSave.destroy()
					self.window.frame_editDef.destroy()
					self.window.frame_editAudioSave.destroy()
					self.window.frame_editAudioReplay.destroy()
					self.window.frame_editReturn.destroy()
					self.window.frame_editDelete.destroy()
					self.currentWindow = 2
					# and then sit edit screen as closed/False
					self.window.displayEditScreen = False
					# self.window.frame_displayeditvoc.destroy()
					# self.window.frame_displayaudioplay.destroy()
				if self.window.lb.curselection() != () and self.window.displayEditScreen == False:
					self.window.frame_displayeditvoc.destroy()
					self.window.frame_displayaudioplay.destroy()

				# self.window.b6.destroy()
				# whole frame
				self.window.myframe.destroy()
				self.window.canvasScroller.destroy()
				self.currentWindow = 0
		
		# elif self.window.displayEditScreen == True:
		# 	self.window.frame_displayeditvoc.destroy()
		# 	self.window.frame_displayaudioplay.destroy()
		
		elif self.currentWindow == 2 and self.window.lb.curselection() != ():
			# IF ON VIEW ALL PAGE, and listbox selection (word selection) isn't empty
			# display that word!
			self.base()
			self.window.button_all_back()
			self.window.screen_viewVocab_displayVocab()
			self.oldSelection = self.window.lb.curselection()


		if self.currentWindow == 0:
			# base screen reload
			self.base()
			self.window.screen_start()



	def base(self):
		width,height = self.width,self.height
		self.canvas.create_rectangle(0,0,width,height,fill=self.window.color_bggray)

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

		# binding onMousePressed to button-1
		self.canvas.bind("<Button-1>", lambda event: self.onMousePressed(event))
		self.window = Window(self.canvas,self.width, self.height,self.cx,self.cy,self.root)

		self.redrawAll()



myapp = LanguageJournal(1*screenWidth,.95*screenHeight)

myapp.run()
