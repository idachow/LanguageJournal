
###########################################
# window.py class for languagejournal_main.py
###########################################

from Tkinter import *
import random
import copy
import time
import csv
import pyaudio
import wave
import sys
import os
import winsound
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

		self.audiostatus = " "

		self.edit = False
		self.audiostring = 0
		self.displayEditScreen = False

		self.color_offwhite = "#D3D5CE"
		self.color_lightteal = "#63DED1"
		self.color_lightorange = "#F1AF8F"
		self.color_darkergray = "#151513"
		self.color_bggray = "#2D2E27"


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

	def updateFileParameters(self):
		with open('data.csv', 'rb') as csvfile:
			r = 0
			filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in filereader:
				if r == self.filerow:
					self.filename = row[1]
					self.filedef = row[2]
					self.filedate = row[0]
				r += 1
		return


	def screen_viewVocab_dataToGrid(self):
		with open('data.csv', 'rb') as csvfile:
			filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
			r = 0
			for row in filereader: 
				r += 1
		with open('data.csv', 'rb') as csvfile:	
			filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
			self.lb = Listbox(self.frameScroller, height=r)
			self.lb.pack()
			for row in filereader:
				self.lb.insert(END,row[1])
		return

	def screen_viewVocab_scroller(self,event):
		cx, cy = self.cx, self.cy
		self.canvasScroller.configure(scrollregion=self.canvasScroller.bbox("all"),width=125,height=cy)


	def screen_viewVocab_displayVocab(self):
		if self.displayEditScreen == True:
			self.frame_editTermSave.destroy()
			self.frame_editTerm.destroy()

		self.displayEditScreen = False

		cx, cy = self.cx, self.cy
		save = self.lb.curselection()
		voc = save[0]
		self.canvas.create_rectangle(cx-25,cy-cy/2-20,self.width,self.height,
									fill=self.color_bggray,outline=self.color_bggray)
		#title
		self.canvas.create_text(cx,50,text="view all entries",font="Calibri 36 bold",
								fill=self.color_lightteal)

		def displayVoc():
			with open('data.csv', 'rb') as csvfile:
				r = 0
				filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in filereader:
					if r == voc:
						self.filename = row[1]
						self.filerow = r
						self.filedef = row[2]
						self.filedate = row[0]
						self.canvas.create_text(cx,cy-cy/2,text=self.filename,font="Calibri 24 bold",
									fill=self.color_lightorange,anchor="w")
						self.canvas.create_text(cx,cy-cy/2+50,text=row[2],font="Calibri 16",
									fill=self.color_offwhite,anchor="w")
					r += 1
			return

		displayVoc()


		self.frame_displayaudioplay=Frame(self.canvas,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_displayaudioplay.place(x=cx,y=cy-cy/2+110)
		self.b5 = Button(self.frame_displayaudioplay,text="Play Recorded Audio", command=lambda:self.interPlayAudio())
		self.b5.pack()
		self.frame_displayeditvoc=Frame(self.canvas,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_displayeditvoc.place(x=cx,y=cy+180)
		self.b6 = Button(self.frame_displayeditvoc,text="EDIT VOCABULARY", command=lambda:self.screen_editVocab())
		self.b6.pack()
		# winsound.Beep(1000, 1000)

		# self.frame_audioplay=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		# self.frame_audioplay.place(x=cx,y=cy+30)
		# self.b3 = Button(self.frame_audioplay,text="play recorded audio", command=lambda:self.playAudio(self.lastadded))
		# self.b3.pack()


	def interPlayAudio(self):
		# winsound.Beep(1000, 1000)
		self.playAudio(self.filename)
		print "filename", self.filename

	def screen_viewVocab(self):
		width = self.width
		height = self.height
		self.canvas.create_rectangle(0,0,width,height,fill="#2D2E27")
		self.button_all_back()
		cx, cy = self.cx, self.cy
		self.canvas.create_text(cx,50,text="View all entries",font="Calibri 36 bold",
								fill=self.color_lightteal)
	

		# adapted from http://stackoverflow.com/questions/16188420/python-tkinter-scrollbar-for-frame
		self.myframe=Frame(self.root,relief=GROOVE,width=25,height=100,bd=1)
		self.myframe.place(x=cx-cx/2,y=cy-cy/2)

		self.canvasScroller=Canvas(self.myframe)
		self.frameScroller=Frame(self.canvasScroller)
		self.myscrollbar=Scrollbar(self.myframe,orient="vertical",command=self.canvasScroller.yview)
		self.canvasScroller.configure(yscrollcommand=self.myscrollbar.set)

		self.myscrollbar.pack(side="right",fill="y")
		self.canvasScroller.pack(side="left")
		self.canvasScroller.create_window((0,0),window=self.frameScroller,anchor='nw')
		self.frameScroller.bind("<Configure>",self.screen_viewVocab_scroller)
		self.screen_viewVocab_dataToGrid()


	def edit_audio():
		self.updateFileParameters()
		os.remove("audio/" + self.filename + ".wav")
		self.set_audio(self.filename,3)


	def screen_editVocab(self):
		self.edit = True
		width = self.width
		height = self.height
		cx,cy = self.cx, self.cy
		# clear out previous display vocab frames
		if self.edit == True:
			self.b5.destroy()
			self.b6.destroy()
			self.frame_displayeditvoc.destroy()
			self.frame_displayaudioplay.destroy()
		# place in back button
		self.button_all_back()
		self.canvas.create_rectangle(cx-25,cy-cy/2-20,self.width,self.height,
									fill=self.color_bggray,outline=self.color_bggray)
		# title
		# self.canvas.create_text(cx,50,text="view all vocab",font="Calibri 36 bold",
		# 						fill=self.color_lightteal)
		# editing text
		self.canvas.create_text(cx,cy-cy/2,text="Editing:",font="Calibri 24 bold",
									fill=self.color_offwhite,anchor="w")
		self.canvas.create_text(cx,cy-cy/2+50,text="'" + self.filename + "'",font="Calibri 24 bold",
									fill=self.color_lightorange,anchor="w")



		def edit_word():
			self.updateFileParameters()
			# index = indexOfEdit
			fetche = self.eEditTerm.get()
			# print str(fetche),str(fetche2)
			# determine what is edited
			# save into CSV
			self.eEditTerm.delete(0,END)
			# print self.newWord
			self.editedWord = Vocab(str(fetche), " ", " ")
			self.editedWord.editWord(fetche,self.filerow,self.filedate,self.filedef,self.filename)

		def edit_def():
			self.updateFileParameters()
			# index = indexOfEdit
			fetche = self.eEditDef.get()
			# print str(fetche),str(fetche2)
			# determine what is edited
			# save into CSV
			self.eEditDef.delete(0,END)
			# print self.newWord
			self.editedDef = Vocab(" ", str(fetche), " ")
			self.editedDef.editDef(fetche,self.filerow,self.filedate,self.filename)

		def edit_return():
			self.canvas.create_rectangle(cx-25,cy-cy/2-20,self.width,self.height,
									fill=self.color_bggray,outline=self.color_bggray)
			self.frame_editTermSave.destroy()
			self.frame_editTerm.destroy()
			self.frame_editDefSave.destroy()
			self.frame_editDef.destroy()
			self.frame_editAudioSave.destroy()
			self.frame_editAudioReplay.destroy()
			self.frame_editReturn.destroy()

			self.displayEditScreen = False

			self.myframe.destroy()
			self.canvasScroller.destroy()

			self.screen_viewVocab()

		# frame for vocab edit entry
		self.canvas.create_text(cx,cy-125,text="Change Vocabulary Term:", fill="white", anchor="w")
		self.frame_editTerm=Frame(self.root,relief=GROOVE,width=0,height=0,bd=1)
		self.frame_editTerm.place(x=cx,y=cy-100)
		# frame for save
		self.frame_editTermSave=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_editTermSave.place(x=cx,y=cy-75)
		# # frame for record

		# frame for entry for vocab term
		self.eEditTerm = Entry(self.frame_editTerm,width=40)
		# self.e2 = Entry(self.frame_entrydefinition, width=100)
		self.eEditTerm.pack()
		# self.e2.pack()
		self.bSaveTerm = Button(self.frame_editTermSave,text="save",command=lambda:edit_word())
		self.bSaveTerm.pack()

		# frame for vocab edit entry
		self.canvas.create_text(cx,cy,text="Change Vocabulary Definition:", fill="white", anchor="w")
		self.frame_editDef=Frame(self.root,relief=GROOVE,width=0,height=0,bd=1)
		self.frame_editDef.place(x=cx,y=cy+25)
		# frame for save
		self.frame_editDefSave=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_editDefSave.place(x=cx,y=cy+50)


		# frame for entry for vocab term
		self.eEditDef = Entry(self.frame_editDef,width=100)
		# self.e2 = Entry(self.frame_entrydefinition, width=100)
		self.eEditDef.pack()
		# self.e2.pack()
		self.bSaveDef = Button(self.frame_editDefSave,text="save",command=lambda:edit_def())
		self.bSaveDef.pack()


		# frame for vocab edit entry
		self.canvas.create_text(cx,cy+125,text="Re-record Audio:", fill="white", anchor="w")
		# frame for save
		self.frame_editAudioSave=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_editAudioSave.place(x=cx,y=cy+150)
		self.frame_editAudioReplay=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_editAudioReplay.place(x=cx,y=cy+180)

		self.bSaveAudio = Button(self.frame_editAudioSave,text="Re-record",command=lambda:self.edit_audio())
		self.bSaveAudio.pack()
		self.bSaveReplay = Button(self.frame_editAudioReplay,text="Replay re-recording",command=lambda:self.playAudio(self.filename))
		self.bSaveReplay.pack()


		self.frame_editReturn=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_editReturn.place(x=cx,y=cy+250)

		self.bReturn = Button(self.frame_editReturn,text="<-- Back",command=lambda:edit_return())
		self.bReturn.pack()

		self.displayEditScreen = True



	def set_audio(self,fileForAudio,seconds):

		# adapted from pyaudio documentation
		CHUNK = 1024
		FORMAT = pyaudio.paInt16
		CHANNELS = 2
		RATE = 44100
		RECORD_SECONDS = seconds
		WAVE_OUTPUT_FILENAME = "audio/" + fileForAudio + ".wav"

		p = pyaudio.PyAudio()

		stream = p.open(format=FORMAT,
						channels=CHANNELS,
						rate=RATE,
						input=True,
						frames_per_buffer=CHUNK)

		print("* recording")
		self.audiostatus = "RECORDING FOR 5 SECONDS..."

		frames = []

		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(data)

		print("* done recording")
		self.audiostatus = "DONE RECORDING!"

		stream.stop_stream()
		stream.close()
		p.terminate()

		wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
		wf.setnchannels(CHANNELS)
		wf.setsampwidth(p.get_sample_size(FORMAT))
		wf.setframerate(RATE)
		wf.writeframes(b''.join(frames))
		wf.close()


	def playAudio(self,wavfile):
		CHUNK = 1024

		print "play: ", wavfile+".wav"
		wf = wave.open("audio/" + wavfile +".wav", 'rb')

		p = pyaudio.PyAudio()

		stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
						channels=wf.getnchannels(),
						rate=wf.getframerate(),
						output=True)

		data = wf.readframes(CHUNK)

		while data != '':
			stream.write(data)
			data = wf.readframes(CHUNK)

		stream.stop_stream()
		stream.close()

		p.terminate()

	def screen_newVocab(self):
		width = self.width
		height = self.height
		self.canvas.create_rectangle(0,0,width,height,fill=self.color_bggray)
		self.button_all_back()

		cx, cy = self.cx, self.cy
		self.canvas.create_text(cx,50,text="Create new entry",font="Calibri 36 bold",fill=self.color_lightteal)
		def set_text():
			fetche = self.e.get()
			fetche2 = self.e2.get()
			# print str(fetche),str(fetche2)
			date = time.strftime("%x")
			print date
			self.newWord = Vocab(str(fetche),str(fetche2),date)
			self.e.delete(0,END)
			self.e2.delete(0,END)
			# print self.newWord
			self.newWord.saveAll()

			self.set_audio(str(fetche),.1)

			with open('data.csv', 'rb') as csvfile:
				filereader = csv.reader(csvfile, delimiter=',', quotechar='|')
				r = 0
				for row in filereader:
					self.lastadded = row[1]
			return

		# frame for vocab entry
		self.canvas.create_text(cx-cx/2,cy-175,text="Vocabulary Term:", fill="white", anchor="w")
		self.frame_entryvocab=Frame(self.root,relief=GROOVE,width=0,height=0,bd=1)
		self.frame_entryvocab.place(x=cx-cx/2,y=cy-150)
		# frame for defintionb
		self.canvas.create_text(cx-cx/2,cy-100,text="Definition:",fill="white",anchor="w")
		self.frame_entrydefinition=Frame(self.root,relief=GROOVE,width=0,height=0,bd=1)
		self.frame_entrydefinition.place(x=cx-cx/2,y=cy-75)
		# frame for save
		self.frame_entrysave=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_entrysave.place(x=cx-cx/2,y=cy-40)


		self.canvas.create_text(cx-cx/2,cy+50,text="Record Audio (only after saving new entry):", 
								fill="white", anchor="w")


		# frame for record
		self.frame_audiosave=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_audiosave.place(x=cx-cx/2,y=cy+75)
		# frame for play
		self.frame_audioplay=Frame(self.root,relief=GROOVE,width=0,height=0,bd=0)
		self.frame_audioplay.place(x=cx-cx/2+150,y=cy+75)

		self.canvas.create_text(cx-cx/2,cy+115,text="Records for 3 seconds",
								fill=self.color_lightteal,font="Calibri 10",anchor="w")

		# NEW FRAME INCLUDES:
		self.e = Entry(self.frame_entryvocab,width=40)
		self.e2 = Entry(self.frame_entrydefinition, width=100)
		self.e.pack()
		self.e2.pack()
		self.b1 = Button(self.frame_entrysave,text="save",command=lambda:set_text())
		self.b2 = Button(self.frame_audiosave,text="record audio",
						command=lambda:self.set_audio(self.lastadded,3))
		self.b3 = Button(self.frame_audioplay,text="play recorded audio", 
						command=lambda:self.playAudio(self.lastadded))
		self.b1.pack()
		self.b2.pack()
		self.b3.pack()
