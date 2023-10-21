# Bazeries
from tools import setManipulator as sm
import random

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
def returnInfo(choice):

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["Bazeries",
		'''Simple subsititution plus transposition''',
		True,
		1,
		[0,1],
		[0,1]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey, needSeed, check):
	genSet = sm.returnSet(0)
	charList = genSet["charList"]
	if(check):
		charList = charList.replace("\t","")
		charList = charList.replace("\n","")
	if(needSeed):
		random.seed(mainkey)

	keyDict = {}
	charRem = charList
	for i in range(len(charList),0,-1):
		if (i == 1 and charRem == charList[0]):
			tempk = list(keyDict.keys())[random.randint(0,(len(keyDict)-1))]
			tempc = keyDict[tempk]
			keyDict[tempk] = charList[0]
			keyDict[charList[0]] = tempc
		else:
			temp = random.randint(0,i-1)
			while (charList[i-1] == charRem[temp]):
				temp = random.randint(0,i-1)
			keyDict[charList[i-1]] = charRem[temp]
			if temp+1 == len(charRem):
				charRem = charRem[:temp]
			else:
				charRem = charRem[:temp] + charRem[temp+1:]

	keyNum = random.randint(2,12)
	return keyNum, keyDict

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey, decrypting = False):
	check = False
	if (text.find("\t")==-1 and text.find("\n")==-1):
		check = True
	key, keyDict = setKey(mainkey, True, check)

	flag = True
	ctext = ""
	textRem = text
	while (flag):
		if (decrypting):
			newDict = {v: k for k, v in keyDict.items()}
			keyDict = newDict
		if (len(textRem)>key):
			tempText = textRem[:key][::-1]
			textRem = textRem[key:]
		else:
			tempText = textRem[::-1]
			flag = False
		for c in tempText:
			ctext += keyDict[c]
		if (flag):
			key, keyDict = setKey(mainkey, False, check)

	if check:
		return ctext, 1
	else:
		return ctext, 0

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	return encrypt(ctext, mainkey, True)