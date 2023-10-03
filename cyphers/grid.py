# Grid Cypher
from tools import setManipulator as sm
import random

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
def returnInfo(choice):
	genSet = sm.returnSet(0)
	charList = genSet["charList"]
	x = 2
	y = 81
	z = len(charList) * 3
	while (z>=y):
		x += 1
		c = x//2
		r = x%2
		f = ""
		b = ""
		for i in range(c):
			if i==0:
				f += "8"
				b += "1"
			else:
				f += "9"
				b += "0"
		if (r==1):
			y = int(f+"9"+b)
		else:
			y = int(f+b)

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["Grid Cypher",
		'''description''',
		False,
		x,
		[0],
		[4]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey):
	ckey = mainkey
	return ckey

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey):
	key = setKey(mainkey)
	ctext = text
	return ctext, 4

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	key = setKey(mainkey)
	text = ctext
	return text, 0