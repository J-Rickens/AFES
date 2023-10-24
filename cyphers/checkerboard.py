# Checkerboard Cypher
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
	
	info = ["Checkerboard Cypher",
		'''description''',
		False,
		2,
		[0],
		[1]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey, needSeed, decrypting):
	genSet = sm.returnSet(0)
	charList = genSet["charList"]
	if (needSeed):
		random.seed(mainkey)

	grid = {}
	cols = []
	rows = []

	maxlen = int(math.sqrt(len(charList))) + 1
	rowlen = random.randint(4,maxlen)
	columnlen = len(charList)//rowlen + 1

	loc = [random.randint(0,rowlen), random.randint(0,columnlen)]
	usedLoc = []
	for c in charList:
		while (loc in usedLoc):
			loc = [random.randint(0,rowlen), random.randint(0,columnlen)]
		usedLoc.append(loc)
		if (decrypting):
			grid[str(loc[0]) + "," + str(loc[1])] = c
		else:
			grid[c] = loc

	modCharList = charList.replace("\n","").replace("\t","")
	totalLen = rowlen+columnlen+2
	letPerNum = len(modCharList)//totalLen
	for i in range(letPerNum):
		for j in range(totalLen):
			c = modCharList[random.randint(0,len(modCharList)-1)]
			modCharList = modCharList.replace(c,"")
			if (j <= rowlen):
				if (i == 0):
					rows.append([c])
				else:
					rows[j].append(c)
			else:
				if (i == 0):
					cols.append([c])
				else:
					cols[j-rowlen-1].append(c)

	return grid, rows, cols


# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey):
	grid, rows, cols = setKey(mainkey, True, False)
	letPerNum = len(rows[0])

	ctext = ""
	i = 0
	for t in text:
		temp = grid[t]
		ctext += rows[temp[0]][random.randint(0, letPerNum-1)]
		ctext += cols[temp[1]][random.randint(0, letPerNum-1)]

		i += 1
		if (i > random.randint(8,20)):
			grid, rows, cols = setKey(mainkey, False, False)
			letPerNum = len(rows[0])
			i = 0

	return ctext, 1

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	grid, rows, cols = setKey(mainkey, True, True)
	letPerNum = len(rows[0])

	text = ""
	i = 0
	for j in range(0,len(ctext),2):
		temp = ""
		for r, row in enumerate(rows):
			if (ctext[j] in row):
				temp = str(r)+","
				break
		for c, col in enumerate(cols):
			if (ctext[j+1] in col):
				temp += str(c)
				break
		text += grid[temp]

		i += 1
		trash = random.randint(0, letPerNum-1)
		trash = random.randint(0, letPerNum-1)
		if (i > random.randint(8,20)):
			grid, rows, cols = setKey(mainkey, False, True)
			letPerNum = len(rows[0])
			i = 0

	return text, 0