#! /usr/bin/env python 3.4



from PIL import Image
import base64
import sys,re
import binascii

filein = open("xml.xml")

data = filein.read()

print(data)

newstring = data.split("</message>")
newstring = newstring[0] + "</message>"

x = re.findall(r'<message type="(.*?)"',newstring)
print(x[0])