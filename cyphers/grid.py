# Grid Cypher
from tools import setManipulator as sm
import random

def gridDigitCount():
	genSet = sm.returnSet(0)
	charList = genSet["charList"]
	digits = 2
	size = 81
	fill = len(charList) * 3
	while (fill>=size):
		digits += 1
		c = digits//2
		r = digits%2
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
			size = int(f+"9"+b)
		else:
			size = int(f+b)
	return digits

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
def returnInfo(choice):
	digits = gridDigitCount()

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["Grid Cypher",
		'''description''',
		False,
		digits,
		[0],
		[4]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey, needSeed, decrypting):
	genSet = sm.returnSet(0)
	charList = genSet["charList"]
	digits = gridDigitCount()
	if (needSeed):
		random.seed(mainkey)

	xdigits = digits // 2
	xmax = ""
	for i in range(xdigits):
		xmax += "9"
	
	ymax = xmax
	ydigits = xdigits
	if (digits%2==1):
		ymax += "9"
		ydigits += 1
	ymax = int(ymax)
	xmin = (len(charList)//ymax) + 1
	if (xmin < 4):
		xmin = 5

	xmax = int(xmax)
	xsize = random.randint(xmin,xmax)
	ysize = (len(charList)//xsize) + 1

	grid = {}
	usedNum = []
	for c in charList:
		flag = True
		while(flag):
			x = str(random.randint(1,xsize))
			y = str(random.randint(1,ysize))
			while(len(x)<xdigits):
				x = "0" + x
			while(len(y)<ydigits):
				y = "0" + y
			gridLoc = x+y
			if gridLoc not in usedNum:
				if (decrypting):
					grid[gridLoc] = c
				else:
					grid[c] = gridLoc
				usedNum.append(gridLoc)
				flag = False
	return grid

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey):
	key = setKey(mainkey, True, False)
	
	resetCount = 0
	resetNum = random.randint(5,15)
	ctext = ""
	for c in text:
		ctext += key[c]

		resetCount += 1
		if (resetCount == resetNum):
			key = setKey(mainkey, False, False)
			resetCount = 0
			resetNum = random.randint(5,15)

	return ctext, 4

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	key = setKey(mainkey, True, True)
	digits = gridDigitCount()

	resetCount = 0
	resetNum = random.randint(5,15)
	text = ""
	for i in range(digits,len(ctext)+1,digits):
		num = ctext[i-digits:i]
		text += key[num]

		resetCount += 1
		if (resetCount == resetNum):
			key = setKey(mainkey, False, True)
			resetCount = 0
			resetNum = random.randint(5,15)

	return text, 0