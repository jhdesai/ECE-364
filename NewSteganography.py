#! /usr/local/bin/python3.4

#$Author: ee364e06 $
#$Date: 2015-04-20 16:39:00 -0400 (Mon, 20 Apr 2015) $
#HeadURL$
#Revision$

#######################################################################
#
#
#	Name : Jakshay Desai
#	Lab Project phase 2
#	Classes NewSteganography implemented
#
#######################################################################

from Steganography import *
from BitVector import *

class NewSteganography(Steganography):


	def __init__(self,imagePath,direction = 'horizontal'):
		Steganography.__init__(self,imagePath,direction)

	def wipeMedium(self):
		data = list(self.im.getdata())

		if self.direction == "vertical":														### Transpose the final matrix when original
			y = []																				### image is extracted vertically in order to
			for i in range(self.x[0]):															### avoid getting an inverted image.
				y = y + data[i::self.x[0]]

			data = y

		for element in range(len(data)):
			if data[element] % 2 == 1:
				data[element] -= 1

		if self.direction == "vertical":														### Transpose the final matrix when original
			y = []																				### image is extracted vertically in order to
			for i in range(self.x[1]):															### avoid getting an inverted image.
				y = y + data[i::self.x[1]]

			data = y


		image = Image.new('L',self.x)
		image.putdata(data)
		image.save("new_h.png")
		image.save(self.imagePath)


	def checkIfMessageExists(self):
		data = list(self.im.getdata())

		if self.direction == "vertical":														### Transpose the final matrix when original
			y = []																				### image is extracted vertically in order to
			for i in range(self.x[0]):															### avoid getting an inverted image.
				y = y + data[i::self.x[0]]

			data = y

		string = ""

		for element in data[0:1000]:																	
			string += str(self.extractlastbit(element))

		intlist = []
		for bits in range(0,len(string),8):
			integer = int(string[bits:bits+8],2)
			intlist.append(integer)

		newstring = ""
		for byte in intlist:
			newstring += chr(byte)

		newstring = newstring.split("</message>")
		newstring = newstring[0] + "</message>"
		#print(newstring)
		x = re.findall(r'<message type=".*?" size=".*?" encrypted=".*?">',newstring)
		if x == []:
			return (False,None)
		else:
			y = re.findall(r'<message type="(.*?)"',newstring)
			return (True,y[0])
