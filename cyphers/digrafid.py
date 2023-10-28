# Digrafid Cypher
from tools import setManipulator as sm
from tools import recTool as rt
import random
import math

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
# all inputRecs are 0 and last outputRec must be 0
def returnInfo(choice):

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["digrafid",
		'''description''',
		False,
		2,
		[0, 0],
		[1, 0]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
# min 27 characters in charList or infinate loop error
def setKey(mainkey, needSeed):
	if (needSeed):
		random.seed(mainkey)
	genSet = sm.returnSet(0)
	charList = genSet["charList"]

	size = int(len(charList)**(1./3))+1
	keyMainTable = [[],[]]
	for i in range(size):
		keyMainTable[0].append([])
		keyMainTable[1].append([])
		for _ in range(size**2):
			keyMainTable[0][i].append("")
			keyMainTable[1][i].append("")

	r1 = random.randint(0,size-1)
	c1 = random.randint(0,(size**2)-1)
	r2 = random.randint(0,size-1)
	c2 = random.randint(0,(size**2)-1)
	for c in charList:
		while(keyMainTable[0][r1][c1] != ""):
			r1 = random.randint(0,size-1)
			c1 = random.randint(0,(size**2)-1)
		while(keyMainTable[1][r2][c2] != ""):
			r2 = random.randint(0,size-1)
			c2 = random.randint(0,(size**2)-1)
		keyMainTable[0][r2][c2] = c
		keyMainTable[1][r2][c2] = c

	size2 = size - 1
	opoI = 0
	modCharList = rt.returnRec(returnInfo(5)[opoI])
	while (len(modCharList) < size2**3):
		opoI += 1
		modCharList = rt.returnRec(returnInfo(5)[opoI])

	keyTables = [[[],[]], [[],[]]]
	usedChars = [["",""],["",""]]

	c1 = modCharList[random.randint(0,len(modCharList)-1)]
	c2 = modCharList[random.randint(0,len(modCharList)-1)]
	c3 = modCharList[random.randint(0,len(modCharList)-1)]
	c4 = modCharList[random.randint(0,len(modCharList)-1)]
	for i in range(size2):
		keyTables[0][0].append([])
		keyTables[0][1].append([])
		keyTables[1][0].append([])
		keyTables[1][1].append([])
		for _ in range(size2**2):
			while(c1 in usedChars[0][0]):
				c1 = modCharList[random.randint(0,len(modCharList)-1)]
			keyTables[0][0][i].append(c1)
			usedChars[0][0] += c1

			while(c2 in usedChars[0][1]):
				c2 = modCharList[random.randint(0,len(modCharList)-1)]
			keyTables[0][1][i].append(c2)
			usedChars[0][1] += c2

			while(c3 in usedChars[1][0]):
				c3 = modCharList[random.randint(0,len(modCharList)-1)]
			keyTables[1][0][i].append(c3)
			usedChars[1][0] += c3

			while(c4 in usedChars[1][1]):
				c4 = modCharList[random.randint(0,len(modCharList)-1)]
			keyTables[1][1][i].append(c4)
			usedChars[1][1] += c4

	keyTables.insert(0, keyMainTable)
	return keyTables, size, opoI

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey):
	keyTables, size, opoI = setKey(mainkey, True)

	textEnd = ""
	if (len(text)%2 == 1):
		textEnd = text[-1]
		text = text[:-1]

	tempTable = [[],[],[]]
	for i in range(0,len(text),2):
		for j, row in enumerate(keyTables[0][0]):
			if (text[i] in row):
				tempTable[0].append(row.index(text[i]))
				tempTable[1].append(j*size)
				break
		for j, row in enumerate(keyTables[0][1]):
			if (text[i+1] in row):
				tempTable[1][i//2] += j
				tempTable[2].append(row.index(text[i+1])) 
				break

	if (len(textEnd) > 0):
		for j, row in enumerate(keyTables[0][0]):
			if (textEnd in row):
				tempTable[0].append(row.index(textEnd))
				tempTable[1].append(j*size)
				break

	keyTables, size, opoI = setKey(mainkey, True)
	size -= 1
	totalIndex = 0
	ctext = ""
	while (totalIndex < len(tempTable[0])):
		interval = random.randint(3,8)
		if (totalIndex+interval < len(tempTable[0])):
			for i in range(0, interval*3, 3):
				r1, c1 = divmod(i,interval)
				r2, c2 = divmod(i+1,interval)
				r3, c3 = divmod(i+2,interval)
				temp = []
				temp.append(tempTable[r1][totalIndex+c1])
				temp.append(tempTable[r2][totalIndex+c2])
				temp.append(tempTable[r3][totalIndex+c3])

				for t in range(len(temp)):
					spliter = 0
					if (temp[t] >= size**2):
						spliter = random.randint(temp[t]-(size**2)+1,(size**2)-1)
					else:
						spliter = random.randint(0,temp[t])
					temp[t] = [spliter,temp[t]-spliter]
				temp.insert(0,[])
				for t in range(2):
					t1, t2 = divmod(temp[2][t], size)
					temp[0].append(t1)
					temp[2][t] = t2

				ctext += keyTables[1][0][temp[0][0]][temp[1][0]]
				ctext += keyTables[1][1][temp[2][0]][temp[3][0]]
				ctext += keyTables[2][0][temp[0][1]][temp[1][1]]
				ctext += keyTables[2][1][temp[2][1]][temp[3][1]]

		else:
			interval = len(tempTable[0]) - totalIndex
			for i in range(0, (interval-1)*3, 3):
				r1, c1 = divmod(i,interval)
				r2, c2 = divmod(i+1,interval)
				r3, c3 = divmod(i+2,interval)
				temp = []
				temp.append(tempTable[r1][totalIndex+c1])
				temp.append(tempTable[r2][totalIndex+c2])
				temp.append(tempTable[r3][totalIndex+c3])

				for t in range(len(temp)):
					spliter = 0
					if (temp[t] >= size**2):
						spliter = random.randint(temp[t]-(size**2)+1,(size**2)-1)
					else:
						spliter = random.randint(0,temp[t])
					temp[t] = [spliter,temp[t]-spliter]
				temp.insert(0,[])
				for t in range(2):
					t1, t2 = divmod(temp[2][t], size)
					temp[0].append(t1)
					temp[2][t] = t2

				ctext += keyTables[1][0][temp[0][0]][temp[1][0]]
				ctext += keyTables[1][1][temp[2][0]][temp[3][0]]
				ctext += keyTables[2][0][temp[0][1]][temp[1][1]]
				ctext += keyTables[2][1][temp[2][1]][temp[3][1]]

			if (len(textEnd) > 0):
				temp = tempTable[2][-2:]
				for t in range(len(temp)):
					spliter = 0
					if (temp[t] >= size**2):
						spliter = random.randint(temp[t]-(size**2)+1,(size**2)-1)
					else:
						spliter = random.randint(0,temp[t])
					temp[t] = [spliter,temp[t]-spliter]
				temp.insert(0,[])
				for t in range(2):
					t1, t2 = divmod(temp[2][t], size)
					temp[0].append(t1)
					temp[2][t] = t2

				ctext += keyTables[1][0][temp[0][0]][temp[1][0]]
				ctext += keyTables[1][1][temp[0][1]][temp[1][1]]
				ctext += keyTables[2][0][temp[2][0]][temp[2][1]]
			else:
				temp = tempTable[2][-3:]
				for t in range(len(temp)):
					spliter = 0
					if (temp[t] >= size**2):
						spliter = random.randint(temp[t]-(size**2)+1,(size**2)-1)
					else:
						spliter = random.randint(0,temp[t])
					temp[t] = [spliter,temp[t]-spliter]
				temp.insert(0,[])
				for t in range(2):
					t1, t2 = divmod(temp[2][t], size)
					temp[0].append(t1)
					temp[2][t] = t2

				ctext += keyTables[1][0][temp[0][0]][temp[1][0]]
				ctext += keyTables[1][1][temp[2][0]][temp[3][0]]
				ctext += keyTables[2][0][temp[0][1]][temp[1][1]]
				ctext += keyTables[2][1][temp[2][1]][temp[3][1]]

		totalIndex += interval

	return ctext, returnInfo(5)[opoI]

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	keyTables, size, _ = setKey(mainkey, True)
	text = ctext
	return text, 0