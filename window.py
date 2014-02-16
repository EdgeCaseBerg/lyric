#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

from array import array

import record
import os

def testShit():
	#record.record_to_file('demo.wav')
	pass

def recordButton():
	recButton = QtGui.QPushButton("Record")
	recButton.setToolTip('Record an audio segment for this Line')
	return recButton

def clearButton():
	clrButton = QtGui.QPushButton("Clear")
	clrButton.setToolTip('Remove audio segment from this line')
	return clrButton

class LineEntry():
	"""Line Entry is a simple panel with a text form and a set of buttons
	   The buttons provide an interface to record a sound clip for that
	   line's text. Remove the sound clip, or save it out to a file by 
	   itself.
	"""
	def __init__(self, rec, clr, edt):
		self.sample_width = 0
		self.sound_data = array('h')
		self.recButton = rec
		self.clrButton = clr 
		self.textEdit = edt
		self.initUI()

	def initUI(self):
		#Implement handlers
		self.recButton.clicked.connect(testShit)
		self.clrButton.clicked.connect(testShit)

	def getText(self):
		return "%s" % self.textEdit.text() #return the text as a python string

	def getSoundData(self):
		return self.sample_width, self.sound_data

class ProgressWindow(QtGui.QMainWindow):
	"""Bell and whistle for reading a file in / saving / etc"""
	def __init__(self):
		super(ProgressWindow, self).__init__()
		self.initUI()

	def initUI(self):
		self.pbar = QtGui.QProgressBar(self)
		self.pbar.setGeometry(30, 40, 200, 25)

		self.setCentralWidget(self.pbar)

		self.setWindowTitle('Lyric is Working')
		self.resize(200,25)

		#Center Window In Screen
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def reset(self):
		self.pbar.setValue(0)

	def setValue(self, val=0):
		self.raise_()
		self.pbar.setValue(val)


class LyricWindow(QtGui.QMainWindow):

	def __init__(self):
		super(LyricWindow, self).__init__()
		self.lines = []
		self.filename = ""
		self.initUI()

	def makeMenu(self):
		exitAction = QtGui.QAction(QtGui.QIcon('icons/exit.png'), '&Exit', self)        
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(QtGui.qApp.quit)

		self.openFile = QtGui.QAction(QtGui.QIcon('icons/open.png'), 'Open', self)
		self.openFile.setShortcut('Ctrl+O')
		self.openFile.setStatusTip('Open new File')
		self.openFile.triggered.connect(self.showDialog)

		self.saveFileAction = QtGui.QAction(QtGui.QIcon('icons/save.png'), 'Save', self)
		self.saveFileAction.setShortcut('Ctrl+S')
		self.saveFileAction.setStatusTip('Save current File')
		self.saveFileAction.triggered.connect(self.saveFile)

		self.saveAsFileAction = QtGui.QAction(QtGui.QIcon('icons/saveas.png'), 'Save As', self)
		self.saveAsFileAction.setShortcut('Ctrl+Shift+S')
		self.saveAsFileAction.setStatusTip('Save as new File')
		self.saveAsFileAction.triggered.connect(self.saveAsFile)

		self.newFile = QtGui.QAction(QtGui.QIcon('icons/icon.png'), 'New', self)
		self.newFile.setShortcut('Ctrl+N')
		self.newFile.setStatusTip('New Lyrics')
		self.newFile.triggered.connect(self.newFileCommand)

		menubar = self.menuBar()

		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(self.newFile)
		fileMenu.addAction(self.openFile)
		fileMenu.addAction(self.saveFileAction)
		fileMenu.addAction(self.saveAsFileAction)
		fileMenu.addAction(exitAction)

	def newFileCommand(self):
		pass

	def initUI(self):
		
		self.makeMenu()

		vbox = QtGui.QVBoxLayout()

		for l in xrange(1,4):
			entryField = QtGui.QLineEdit()
			recButton = recordButton()
			clrButton = clearButton()
			
			hbox = QtGui.QHBoxLayout()
			hbox.addStretch(1)
			hbox.addWidget(entryField)
			hbox.addWidget(recButton)
			hbox.addWidget(clrButton)	
			vbox.addStretch(1)

			entry = LineEntry(recButton,clrButton,entryField)
			vbox.addLayout(hbox)
			self.lines.append(entry)
		
		frame = QtGui.QWidget()
		frame.setLayout(vbox)
		self.setCentralWidget(frame)
		
		self.resize(500,350)
		#Center Window In Screen
		qr = self.frameGeometry()
		cp = QtGui.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

		self.setWindowTitle('Lyric')
		self.setWindowIcon(QtGui.QIcon('icons/icon.png'))
		self.statusBar()

		self.displayStatus('Ready')

		self.show()
		self.pbar = ProgressWindow()


	#Catch the X on the window
	def closeEvent(self, event):
		self.displayStatus('Displaying Dialog')

		reply = QtGui.QMessageBox.question(self, 'Are you sure?',
			"Are you sure you want to quit?", QtGui.QMessageBox.Yes | 
			QtGui.QMessageBox.No, QtGui.QMessageBox.No)

		if reply == QtGui.QMessageBox.Yes:
			self.displayStatus('quiting')
			event.accept()
		else:
			self.displayStatus('Ready')
			event.ignore()  


	def displayStatus(self, strMessage = ""):
		self.statusBar().showMessage(strMessage)

	def showDialog(self):
		if(self.sender() == self.openFile):
			self.pbar.reset()
			fname = QtGui.QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser('~'))
			
			f = open(fname, 'r')
			with f:        
				print f.name
				self.filename = f.name
				self.pbar.show()
				val = 0
				for line in f:
					#implement file load / creation here and increment val
					val = val + 1
					self.pbar.setValue(val)

			self.pbar.setValue(100)
			self.pbar.hide()

	def saveAsFile(self):
		filename = QtGui.QFileDialog.getSaveFileName(self, 'Save File', os.path.expanduser('~'))
		f = open(filename, 'w')
		filedata = ""
		f.write(filedata)
		f.close()

	def saveFile(self):
		if(self.filename != ""):
			f = open(self.filename, 'w')
			filedata = ""
			f.write(filedata)
			f.close()



def main():
	
	app = QtGui.QApplication(sys.argv)
	lw = LyricWindow()
	sys.exit(app.exec_())


if __name__ == '__main__':
	main()