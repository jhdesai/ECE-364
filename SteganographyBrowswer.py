#! /usr/local/bin/python3.4

#$Author: ee364e06 $
#$Date: 2015-04-20 16:36:29 -0400 (Mon, 20 Apr 2015) $
#HeadURL$
#Revision$

#######################################################################
#
#
#	Name : Jakshay Desai
#	Lab Project phase 2
#	Classes SteganographygGUI implemented
#
#######################################################################

from PySide.QtCore import *
from PySide.QtGui import *
import re,sys,glob
from SteganographyGUI import *
from NewSteganography import *
from PIL import Image
import copy

class SteganographyGUI(QMainWindow,Ui_MainWindow):
	def __init__(self,parent = None):
		super(SteganographyGUI,self).__init__(parent)
		self.setupUi(self)

		filepath = QFileDialog.getExistingDirectory(self,"open folder only",Options = QFileDialog.ShowDirsOnly)
		if not filepath:
			sys.exit(1)

		self.selectedfile = ""
		self.path = filepath
		newfilepath = str(filepath).split("/")
		filesd = newfilepath[-1]
		self.fileTreeWidget.setHeaderLabel(newfilepath[-1])									### Labelling the treewidget with 
		self.scn = QGraphicsScene()															### the file path
		self.btnExtract.clicked.connect(self.extract)
		self.btnExtract.setEnabled(False)
		self.btnWipeMedium.setEnabled(False)
		self.viewMedium.setEnabled(False)
		self.viewMessage.setEnabled(False)
		self.lblImageMessage.setEnabled(False)

		blue = []
		vertical = []
		horizontal = []
		files = glob.glob(str(filepath)+"/*.png")
		for f in files:																		### Sorting the files as per image
			f = f.split("/")[-1]															### content and the method in which
			y = re.findall('(v|h)',f)														### the message is saved
			if not y:																		### E.g horizontal or vertical
				blue.append(f)
			elif y[0] == 'v':
				im = Image.open(str(filepath)+"/"+f)
				if im.mode == 'L':
					vertical.append(f)
				else:
					blue.append(f)
			elif y[0] == 'h':
				im = Image.open(str(filepath)+"/"+f)
				if im.mode == 'L':
					horizontal.append(f)
				else:
					blue.append(f)

		self.b = blue
		self.v = copy.deepcopy(vertical)
		self.h = copy.deepcopy(horizontal)
		self.dict = {}																		### Creating a dictionary that holds
																							### all the message images and the type
		self.blueitems = []																	### messages they contain if any
		for f in range(len(blue)):
			item = QTreeWidgetItem()
			item.setText(0,"{0}".format(blue[f]))											### Create item widgets for files with
			item.setForeground(0,QtGui.QBrush(Qt.blue))										### no content in them
			self.blueitems.append(item)
			self.dict[blue[f]] = "0"

		x = f + 1
		self.verticalitems = []
		for f in range(len(vertical)):														### Create a list of item widgets from
			item = QTreeWidgetItem(["{0}".format(vertical[f])])								### message mediums that have vertical
			class1 = NewSteganography(str(filepath+"/" + vertical[f]),'vertical')			### messages embedded in them.
			tup = class1.checkIfMessageExists()
			if tup[0]:
				item.addChild(QTreeWidgetItem([tup[1]]))
				self.dict[vertical[f]] = tup[1]
				item.setForeground(0,QtGui.QBrush(Qt.red))
				self.verticalitems.append(item)
			else:
				self.dict[vertical[f]] = tup[1]
				item.setForeground(0,QtGui.QBrush(Qt.blue))
				self.blueitems.append(item)
				self.v.remove(vertical[f])

		for f in range(len(self.verticalitems)):
			self.fileTreeWidget.addTopLevelItem(self.verticalitems[f])

		x += f + 1
		self.horizontalitems = []
		for f in range(len(horizontal)):													### Create a list of item widgets from
			item = QTreeWidgetItem(["{0}".format(horizontal[f])])							### message mediums that have horizontal
			class1 = NewSteganography(str(filepath+"/" + horizontal[f]),'horizontal')		### messages embedded in them.
			tup = class1.checkIfMessageExists()
			if tup[0]:
				item.addChild(QTreeWidgetItem([tup[1]]))
				self.dict[horizontal[f]] = tup[1]
				item.setForeground(0,QtGui.QBrush(Qt.red))
				self.horizontalitems.append(item)

			else:
				self.dict[horizontal[f]] = tup[1]
				item.setForeground(0,QtGui.QBrush(Qt.blue))
				self.blueitems.append(item)
				self.h.remove(horizontal[f])

		for f in range(len(self.horizontalitems)):
			self.fileTreeWidget.addTopLevelItem(self.horizontalitems[f])

		for f in range(len(self.blueitems)):
			self.fileTreeWidget.insertTopLevelItem(f,self.blueitems[f])
		
		self.fileTreeWidget.itemSelectionChanged.connect(self.blueClick)
		self.btnExtract.clicked.connect(self.extract)
		self.btnWipeMedium.clicked.connect(self.wipe)


	### If the selected item on the GUI has been commanded to be wiped off
	### then this function is called which erases the medium and updates the
	### GUI

	def wipe(self):
		box = QMessageBox()																	### Creates a cautionary message box
		reply = box.question(None,"Caution","Wiped message cannot be recovered.Do you want to proceed?",QMessageBox.Ok | QMessageBox.Cancel)
		if reply == QMessageBox.Ok:															### If okay is pressed execute the below code
			if self.selectedfile in self.v:													
				class1 = NewSteganography(self.path+"/"+self.selectedfile,"vertical")
				class1.wipeMedium()															### if the item has vertically embedded
				self.v.remove(self.selectedfile)											### message then wipe the message
				self.btnExtract.setEnabled(False)											### and remove the item and its child from
				self.btnWipeMedium.setEnabled(False)										### tree widget
				item = QTreeWidgetItem([self.selectedfile])
				olditem = self.fileTreeWidget.selectedItems()[0]
				child = olditem.takeChildren()
				self.dict[self.selectedfile] = "0"
				self.fileTreeWidget.takeTopLevelItem(self.fileTreeWidget.indexOfTopLevelItem(olditem))
				item.setText(0,"{0}".format(olditem.text(0)))
				item.setForeground(0,QtGui.QBrush(Qt.blue))
				self.blueitems.append(item)
				self.fileTreeWidget.addTopLevelItem(item)
				self.fileTreeWidget.removeItemWidget(item,0)
			else:
				class1 = NewSteganography(self.path+"/"+self.selectedfile,"horizontal")
				class1.wipeMedium()															### if the item has horizontally embedded
				self.h.remove(self.selectedfile)											### message then wipe the message and
				self.btnExtract.setEnabled(False)											### remove the item and its child from the
				self.btnWipeMedium.setEnabled(False)										### tree widget
				item = QTreeWidgetItem([self.selectedfile])
				olditem = self.fileTreeWidget.selectedItems()[0]
				child = olditem.takeChildren()
				self.dict[self.selectedfile] = "0"
				self.fileTreeWidget.takeTopLevelItem(self.fileTreeWidget.indexOfTopLevelItem(olditem))
				item.setText(0,"{0}".format(olditem.text(0)))
				item.setForeground(0,QtGui.QBrush(Qt.blue))
				self.blueitems.append(item)
				self.fileTreeWidget.addTopLevelItem(item)
				self.fileTreeWidget.removeItemWidget(item,0)
			self.extract()



	### For the selected item in the GUI if the extract button is
	### pressed, this function is called and the embedded message
	### is extracted from the selected item

	def extract(self):
		self.btnExtract.setEnabled(False)
		self.txtMessage.setPlainText("")
		self.scn.clear()
		self.viewMessage.update()
		if self.selectedfile in self.v:														### Instantiate a class based on the method
			class1 = NewSteganography(self.path+"/"+self.selectedfile,"vertical")			### in which the message has been embedded in
		else:																				### the medium
			class1 = NewSteganography(self.path+"/"+self.selectedfile,"horizontal")

		tup = class1.checkIfMessageExists()													### if the message exists then display the
		message = class1.extractMessageFromMedium()											### message on the stack widget using the
		self.viewMessage.setEnabled(True)													### appropriate widget
		self.lblImageMessage.setEnabled(True)
		if tup[1] == "Text":
			self.stackMessage.setCurrentIndex(1)											### Also update the message label below the
			self.lblImageMessage.setText("Text")											### stacked widget
			message.saveToTarget("save.txt")
			filein = open("save.txt")
			data = filein.read()
			self.txtMessage.setPlainText(data)
		elif tup[1] == 'ColorImage' or tup[1] == 'GrayImage':
			self.stackMessage.setCurrentIndex(0)
			self.lblImageMessage.setText("Image")
			message.saveToTarget("save.png")
			self.viewMessage.setScene(self.scn)
			pixmap = QtGui.QPixmap("save.png")
			PixItem = self.scn.addPixmap(pixmap)

			self.viewMessage.fitInView(PixItem)
			self.viewMessage.show()


	### IF any item on the tree widget is selected this function is
	### called and updates the GUI based on the type of item selected

	def blueClick(self):																	
		self.txtMessage.setPlainText("")
		self.scn.clear()
		self.viewMessage.update()
		self.btnExtract.setEnabled(False)
		self.btnWipeMedium.setEnabled(False)
		clicked = self.sender()
		for element in clicked.selectedItems():												### Checks for the selected items
			self.selectedfile = element.text(0)

		if self.selectedfile not in self.dict:
			return

		self.viewMedium.setEnabled(True)													### Enables the medium widget
		if self.dict[self.selectedfile] == 'ColorImage' or self.dict[self.selectedfile] == 'GrayImage':
			self.stackMessage.setCurrentIndex(0)											### Based on the type of embedded
			self.lblImageMessage.setText("Image")											### message, updates the stacked
		else:																				### Widget
			self.stackMessage.setCurrentIndex(1)
			self.lblImageMessage.setText("Text")

		if (self.selectedfile in self.h) or (self.selectedfile in self.v):					### Enable appropriate buttons and 
			self.btnExtract.setEnabled(True)												### labels
			self.btnWipeMedium.setEnabled(True)
			self.viewMessage.setEnabled(True)
		
		scn = QGraphicsScene()																### Create a scene for the graphics view
		self.viewMedium.setScene(scn)														### Set the scene create on the view

		pixmap = QtGui.QPixmap(self.path+"/"+self.selectedfile)							
		PixItem = scn.addPixmap(pixmap)													

		self.viewMedium.fitInView(PixItem)													### Fit the image in the graphics view
		self.viewMedium.show()																### Display the message


if __name__ == "__main__":
	currentApp = QApplication(sys.argv)
	currentForm = SteganographyGUI()
	currentForm.show()
	currentApp.exec_()