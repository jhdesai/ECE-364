#! /usr/local/bin/python3.4

#$Author: ee364e06 $
#$Date: 2015-04-20 16:36:15 -0400 (Mon, 20 Apr 2015) $
#HeadURL$
#Revision$

#######################################################################
#
#
#	Name : Jakshay Desai
#	Classes Message and Steganography implemented
#
#
#	Note : This Script requires the python Bitvector moddule
#
#######################################################################

import re,sys
sys.path.append( "/home/ecegrid/a/ee364e06/Downloads/BitVector-3.3.2" )
from PIL import Image
import base64
import math
from pprint import pprint as pp
from BitVector import *

class Message():
	def __init__(self, **kwargs):
		self.encoded = ""
		self.XmlString = ''
		if len(kwargs) is 2:
			if 'filePath' not in kwargs or 'messageType' not in kwargs:
				raise ValueError("One of the arguments is missing\n")
			if re.match(r'(Text|GrayImage|ColorImage)',kwargs['messageType']):
				pass
			else:
				raise ValueError("Message type incorrect\n")

			if kwargs['filePath'] == '' or kwargs['messageType'] == '':
				raise ValueError("Invalid initializer")
			self.filePath = kwargs['filePath']
			self.messageType = kwargs['messageType']
			self.getXmlString()

		elif len(kwargs) is 1:
			if 'xmlString' not in kwargs or kwargs['xmlString'] == '':
				raise ValueError("Incorrect keys present")
			self.XmlString = kwargs['xmlString']

		else:
			raise ValueError("Incorrect initializer")


	# Returns the size of an xml file in bytes
	def getMessageSize(self):
		if self.XmlString is None:
			raise Exception("No data exists in the instance")
		x = sys.getsizeof(self.XmlString) 
		return x


	# Saves the data contained in an XML string to the appropriate file
	def saveToImage(self, targetImagePath):
		data = self.XmlString.split('\n')
		data = data[1]																					
		size = re.findall(r'<\w*\s*\w*="\w*"\s*\w*="(\w*,\w*|\w*)"',data)						### Get the size of the data
		size = size[0].split(",")
		data = re.findall(r'<\w*\s\w*="(\w*)"',data)											### Find the type of message
		aaa = data[0]
		if data[0] == 'Text':
			raise TypeError("File is not text type")
		with open(targetImagePath,'w') as fileout:
			
			data = self.XmlString.split('\n')
			data = data[2]																		### Checks for validity of data
			if data == '':
				raise Exception("No data exists")

			if aaa == "GrayImage":
				decoded = base64.b64decode(data)												### If message type is grayimage -
				image = Image.frombytes('L',(int(size[0]),int(size[1])),decoded)				### Simply decode data and save it in a file
				image.save(targetImagePath)

			if aaa == "ColorImage":																### if message type is colorimage -
				rgblist = list(base64.b64decode(data))											### we first need to decode the data received -
				r = rgblist[:int(len(rgblist)/3)]												### split the decoded data into red, green and -
				g = rgblist[int(len(rgblist)/3):int(len(rgblist)*2/3)]							### blue pixels
				b = rgblist[int(len(rgblist)*2/3):]																	

				list1 = []
				for i in range(len(r)):
					list1.append((r[i],g[i],b[i]))												### concatenate the pixels and recreate the image
				image = Image.new('RGB',(int(size[0]),int(size[1])))
				image.putdata(list1)
				image.save(targetImagePath)

				


	def saveToTextFile(self,targetTextFilePath):
		data = self.XmlString.split("\n")
		data = data[1]
		data = re.findall(r'<\w*\s\w*="(\w*)"',data)
		if data[0] == 'Text':
			pass
		else:
			raise TypeError("File is not text type")
		with open(targetTextFilePath,'w') as fileout:											### simply decode base64 data and recreate text file
			data = self.XmlString.split('\n')
			data = data[2]
			if data == '':
				raise Exception("No data exists")

			data1 = base64.b64decode(data)
			data = str(data1)[2:-1]
			data = re.sub(r'\\n',r'\n',data)
			fileout.write(data)


	### Calls the appropriate saving function based on the message type specified
	### in the xml string
	def saveToTarget(self, targetPath):
		data = self.XmlString.split("\n")
		data = data[1]
		data = re.findall(r'<\w*\s\w*="(\w*)"',data)
		if data[0] == 'Text':
			self.saveToTextFile(targetPath)
		elif data[0] == 'ColorImage' or data[0] == 'GrayImage':
			self.saveToImage(targetPath)

	### Creates an xml string for a given message medium
	def getXmlString(self):
		if self.messageType == "GrayImage":														### For a grayimage, extract the data in the image -
			im = Image.open(self.filePath)														### as a list of integers.
			self.x = im.size
			data = list(im.getdata())											
			list1 = data
			'''for row in range(self.x[1]):
				for column in range(self.x[0]):
					list1.append(data[column,row])'''
			

			string = ""																			### For every integer in the list find its ascii -
			for element in list1:																### value and concatenate it to a string
				string += chr(element)


			encoded = str(base64.b64encode(bytes(list1)))										### Encode the string generated and base64 encode it
			encoded = re.sub(r"(b'|')","",str(encoded))
			self.XmlString = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
			self.XmlString += "<message type=\"{0}\" size=\"{1},{2}\" encrypted=\"False\">\n".format(self.messageType,self.x[0],self.x[1])
			self.XmlString += "{0}\n".format(encoded)
			self.XmlString += "</message>"

		elif self.messageType == "Text":
			filein = open(self.filePath)
			data = filein.read()																### For text simply extract the data from the file
			encoded = base64.b64encode(bytes(data,'UTF-8'))										### base64 encode it and create an xml string
			encoded = re.sub(r"(b'|')","",str(encoded))
			self.XmlString = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
			self.XmlString += "<message type=\"{0}\" size=\"{1}\" encrypted=\"False\">\n".format(self.messageType,len(data))
			self.XmlString += "{0}\n".format(encoded)
			self.XmlString += "</message>"

		elif self.messageType == "ColorImage":
			im = Image.open(self.filePath)
			self.x = im.size
			data = list(im.getdata())
			list1 = data
			'''for row in range(self.x[1]):
				for column in range(self.x[0]):
					list1.append(data[column,row])'''

			red = []																			### For colorimages the process is the same -
			green = []																			### however instead of list of integers we have
			blue = []																			### we have a list of tuples
			list2 = []
			for element in list1:
				red.append(element[0])
				green.append(element[1])
				blue.append(element[2])

			list2 = red + green+ blue															### Extract each element of tuple individually
																								### into a list and concatenate all the lists
			'''encoded1 = base64.b64encode(bytes(red))
			encoded1 = re.sub(r"(b'|')","",str(encoded1))

			encoded2 = base64.b64encode(bytes(green))
			encoded2 = re.sub(r"(b'|')","",str(encoded2))

			encoded3 = base64.b64encode(bytes(blue))
			encoded3 = re.sub(r"(b'|')","",str(encoded3))'''


			encoded =  base64.b64encode(bytes(list2))											### Base64 encode the entire list
			encoded = re.sub(r"(b'|')","",str(encoded))
			self.XmlString = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
			self.XmlString += "<message type=\"{0}\" size=\"{1},{2}\" encrypted=\"False\">\n".format(self.messageType,self.x[0],self.x[1])
			self.XmlString += "{0}\n".format(encoded)
			self.XmlString += "</message>"

		else:
			raise Exception("No data exists")

		return self.XmlString


class Steganography():

	def __init__(self, imagePath,direction = 'horizontal'):
		if type(imagePath) is not str:
			raise ValueError("imagePath is not string")

		if direction == 'horizontal' or direction == 'vertical':
			pass
		else:
			raise ValueError
		self.im = Image.open(imagePath)
		if self.im.mode != 'L':
			raise TypeError("Medium image is not Gray-scale Image")

		self.imagePath = imagePath
		self.direction = direction
		self.x = self.im.size
		bytes = (self.x[0] - 1) * self.x[1]
		self.maxsize = bytes/8

	def embedMessageInMedium(self,message,targetImagePath):
		
		if message.getMessageSize() > self.maxsize:
			raise ValueError("message size is greater than what the medium image can hold")

		data = list(self.im.getdata())
		medium = data

		if self.direction == "vertical":														### Vertical extraction of the Image medium
			y = []
			for i in range(self.x[0]):
				y = y + medium[i::self.x[0]]

			medium = y


		string1 = str(BitVector(textstring = message.XmlString))

		i = 0
		for bit in range(len(string1)):															### Replace the last bit of each 8-bit integer
			if string1[bit] == str(1):															### in the medium list with a bit of the bitstring
				if medium[bit] % 2 == 0:
					medium[bit] += 1
					i +=1
				elif medium[bit] % 2 == 1:
					i +=1
					pass

			if string1[bit] == str(0):
				if medium[bit] % 2 == 0:
					i +=1
					pass
				elif medium[bit] % 2 == 1:
					medium[bit] -= 1
					i +=1


		'''if self.direction == "vertical":
			for column in range(self.x[1]):
				listnew = []
				for row in range(self.x[0]):
					listnew.append(medium[i])
					i += 1
				y.append[]'''


		if self.direction == "vertical":														### Transpose the final matrix when original
			y = []																				### image is extracted vertically in order to
			for i in range(self.x[1]):															### avoid getting an inverted image.
				y = y + medium[i::self.x[1]]

			medium = y

		image = Image.new('L',self.x)
		image.putdata(medium)
		image.save(targetImagePath)


	def extractMessageFromMedium(self):
		data =	list(self.im.getdata())
		medium = data

		if self.direction == "vertical":														### For vertical image extraction
			y = []
			for i in range(self.x[0]):
				y = y + medium[i::self.x[0]]

			medium = y

		string = ""																				### Extract the last bit of each 
		for element in medium:																	### integer in the image medium
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
		k = re.findall(r'<message',newstring)
		if k == []:																				### if data isn't valid return none
			return None

		'''k = newstring.split("\n")
		k = re.findall(r'\+',k[2])
		if k == []:
			pass
		else:
			return None'''
		message = Message(xmlString=newstring)
		return message


	## I first tried to convert the XMl string using this 
	## function. However I realised that the XML string
	## wouldn't result in the correct bit pattern using
	## this function
	def bini(self,i):
		n = 8
		s = ''
		while n:
			if i & 1 == 1:
				s = "1" + s
			else:
				s = "0" + s
				i >>= 1
			n -= 1

		return s

	## Extracts the last bit of each integer
	def extractlastbit(self,i):
		if i & 1 == 1:
			return 1

		if i & 1 == 0:
			return 0


def main():
	pass
	


if __name__ == "__main__":
	main()