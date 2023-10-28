# Bifid Cypher
from tools import setManipulator as sm
import random
import math

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
def returnInfo(choice):

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["bifid",
		'''description''',
		False,
		1.5,
		[0],
		[0]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey, needSeed):
	if (needSeed):
		random.seed(mainkey)
	genSet = sm.returnSet(0)
	charList = genSet["charList"]

	keyTables = {}
	sizes = []
	while (len(charList)>=4):
		sizes.append(int(math.sqrt(len(charList))))
		for row in range(sizes[-1]):
			for col in range(sizes[-1]):
				c = charList[random.randint(0,len(charList)-1)]
				keyTables[c] = [row, col, len(sizes)-1]
				temp = str(row) + "," + str(col) + "," + str(len(sizes)-1)
				keyTables[temp] = c
				charList = charList.replace(c,"")
	if (len(charList) > 0):
		sizes.append(0)
		for i in range(len(charList)):
			c = charList[random.randint(0,len(charList)-1)]
			keyTables[c] = [0, i, len(sizes)-1]
			temp = "0," + str(i) + "," + str(len(sizes)-1)
			keyTables[temp] = c
			charList = charList.replace(c,"")

	return keyTables

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey):
	keyTables = setKey(mainkey, True)

	tempTable = [[],[],[]]
	i = 0
	for c in text:
		for j in range(3):
			tempTable[j].append(keyTables[c][j])

		i += 1
		if (i >= random.randint(8,30)):
			keyTables = setKey(mainkey, False)
			i = 0

	keyTables = setKey(mainkey, True)
	temp = []
	ctext = ""
	i = 0
	for row in tempTable:
		for col in row:
			temp.append(str(col))
			if (len(temp) == 2):
				temp.append("0")
				ctext += keyTables[",".join(temp)]
				temp.clear()

				i += 1
				if (i >= random.randint(1,3)):
					keyTables = setKey(mainkey, False)
					i = 0

	if (len(temp) == 1):
		temp.extend(["0","0"])
		ctext += keyTables[",".join(temp)]

	return ctext, 0

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	keyTables = setKey(mainkey, True)

	chars = (len(ctext)*2)//3
	tempTable = [[],[],[]]
	counter = 0
	tableSecifier = 0
	i = 0
	for c in ctext[:-1]:
		for j in range(2):
			tempTable[tableSecifier].append(keyTables[c][j])
			counter += 1
			if (counter == chars):
				tableSecifier += 1
				counter = 0

		i += 1
		if (i >= random.randint(1,3)):
			keyTables = setKey(mainkey, False)
			i = 0

	tempTable[2].extend(keyTables[ctext[-1]])

	keyTables = setKey(mainkey, True)
	text = ""
	i = 0
	for j in range(len(tempTable[0])):
		temp = str(tempTable[0][j]) + "," + str(tempTable[1][j]) + "," + str(tempTable[2][j])
		text += keyTables[temp]

		i += 1
		if (i >= random.randint(8,30)):
			keyTables = setKey(mainkey, False)
			i = 0

	return text, 0