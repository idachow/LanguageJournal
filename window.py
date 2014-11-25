
###########################################
# window.py class for languagejournal_main.py
###########################################

from Tkinter import *
import random
import copy
import time
import csv
from eventBasedAnimationClass import EventBasedAnimationClass

from vocab import Vocab

class Window(object):
	def __init__(self,canvas,width,height,cx,cy,root):
		self.canvas = canvas
		self.width = width
		self.height = height
		self.cx = cx
		self.cy = cy
		self.root = root

		self.color_offwhite = "#D3D5CE"
		self.color_lightteal = "#63DED1"
		self.color_lightorange = "#F1AF8F"
		self.color_darkergray = "#151513"


	def button_all_back(self): 
		y = self.height/20
		x = self.height/20
		self.canvas.create_rectangle(x,y,x+100,y+100,fill=self.color_darkergray)
		self.canvas.create_text(x+50,y+50,text="<--",font="Calibri 36 bold",fill=self.color_lightteal)


	def button_start_plus(self):
		cx, cy = self.cx, self.cy
		self.canvas.create_text(cx,cy-(.25*self.height),text="Language Journal", font="Calibri 24 bold",fill=self.color_offwhite)
		self.canvas.create_rectangle(cx+10,cy+50,cx+110,cy-50,fill=self.color_darkergray)
		self.canvas.create_text(cx+60,cy,text="+",font="Calibri 36 bold",fill=self.color_lightteal)

	def button_start_view(self):
		cx, cy = self.cx, self.cy
		self.start_viewbutton_x1 = cx-110
		self.start_viewbutton_x2 = cx-10
		self.start_viewbutton_y1 = cy-50
		self.start_viewbutton_y2 = cy+50
		self.canvas.create_text(cx,cy-(.25*self.height),text="Language Journal", font="Calibri 24 bold",fill=self.color_offwhite)
		self.canvas.create_rectangle(cx-10,cy+50,cx-110,cy-50,fill=self.color_darkergray)
		self.canvas.create_text(cx-60,cy-50,text="___",font="Calibri 30 bold",fill=self.color_lightteal)
		self.canvas.create_text(cx-60,cy-20,text="___",font="Calibri 30 bold",fill=self.color_lightteal)
		self.canvas.create_text(cx-60,cy+10,text="___",font="Calibri 30 bold",fill=self.color_lightteal)


	def screen_start(self):
		self.button_start_view()
		self.button_start_plus()

	def screen_viewVocab(self):
		width = self.width
		height = self.height
		self.canvas.create_rectangle(0,0,width,height,fill="#2D2E27")
		self.button_all_back()
		cx, cy = self.cx, self.cy

		r = 0	
		with open('data.csv', 'rb') as csvfile:
			filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
			# for row in spamreader:
			for row in filereader:
				rowtext = ""
				r += 1
				for col in xrange(3):
					rowtext += row[col]
					rowtext += " | "
				self.canvas.create_text(cx,(height/10)*r+cy/2,text=rowtext,fill=self.color_offwhite)

	

	def screen_newVocab(self):
		width = self.width
		height = self.height
		self.canvas.create_rectangle(0,0,width,height,fill="#2D2E27")
		self.button_all_back()

		cx, cy = self.cx, self.cy
		self.canvas.create_text(cx,cy,text="create new vocab",font="Calibri 36 bold",fill=self.color_lightteal)
		def set_text():
			fetche = e.get()
			fetche2 = e2.get()
			# print str(fetche),str(fetche2)
			date = time.strftime("%x")
			print date
			self.newWord = Vocab(str(fetche),str(fetche2),date)
			e.delete(0,END)
			e2.delete(0,END)
			# print self.newWord
			self.newWord.saveAll()
			return
		e = Entry(self.root,width=40)
		e2 = Entry(self.root, width=100)
		e.pack()
		e2.pack()
		b1 = Button(self.root,text="save",command=lambda:set_text())
		b1.pack()
		