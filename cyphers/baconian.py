# Baconian Cypher
from tools import setManipulator as sm
from tools import recTool as rt
import random

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
def returnInfo(choice):

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["baconian",
		'''description''',
		False,
		4,
		[0],
		[1]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey, needSeed, decrypting = False):
	if (needSeed):
		random.seed(mainkey)
	genSet = sm.returnSet(0)
	charList = genSet["charList"]
	modCharList = rt.returnRec(returnInfo(5)[0])
	binLength = returnInfo(3)
	
	base = 2
	while (len(charList) >= base**binLength):
		base += 1

	keyRep = []
	for b in range(base):
		keyRep.append([])
	keyDict = {}

	usedNum = []
	num = random.randint(0,(base**binLength)-1)
	for c in charList:
		while (num in usedNum):
			num = random.randint(0,(base**binLength)-1)
		usedNum.append(num)
		
		bnum = ""
		temp = num
		while (temp > 0):
			temp, r = divmod(temp,base)
			bnum = str(r) + bnum
		while (len(bnum) < binLength):
			bnum = "0" + bnum

		if (decrypting):
			keyDict[bnum] = c
		else:
			keyDict[c] = bnum
		if (c in modCharList):
			keyRep[random.randint(0,base-1)].append(c)

	return keyDict, keyRep

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey):
	keyDict, keyRep = setKey(mainkey, True)

	ctext = ""
	i = 0
	for c in text:
		temp = keyDict[c]
		for n in range(len(temp)):
			ctext += keyRep[int(temp[n])][random.randint(0,len(keyRep[int(temp[n])])-1)]

		i += 1
		if (i > random.randint(8,20)):
			keyDict, keyRep = setKey(mainkey, False)
			i = 0

	return ctext, returnInfo(5)[0]

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	keyDict, keyRep = setKey(mainkey, True, True)
	binLength = returnInfo(3)
	
	text = ""
	i = 0
	for c in range(binLength,len(ctext)+1,binLength):
		ctemp = ctext[c-binLength:c]
		temp = ""
		for n in ctemp:
			for k, rep in enumerate(keyRep):
				if (n in rep):
					temp += str(k)
					random.randint(0,len(rep)-1)
					break

		text += keyDict[temp]

		i += 1
		if (i > random.randint(8,20)):
			keyDict, keyRep = setKey(mainkey, False, True)
			i = 0

	return text, 0