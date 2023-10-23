# XOR cypher
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
	digits = len(bin(len(charList)-1)[2:])
	x = float(digits)/float(digits-1.0)

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["XOR Cypher",
		'''description''',
		False,
		x,
		[0],
		[1]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey):
	genSet = sm.returnSet(0)
	charList = genSet["charList"]
	random.seed(mainkey)

	digits = len(bin(len(charList)-1)[2:])
	splitvalue = 0
	splitSize = 0
	binLength = bin(len(charList)-1)[3:]
	if (binLength[-1] == "1" and binLength.replace('0','') == "1"):
		splitvalue = 2**(digits-2)
		splitSize = 2
	else:
		splitvalue = 2**(digits-1)
		splitSize = 1
	maxvalue = (2**digits)-1
	ckey = {}
	ckeyInv = {}
	usedNum = []

	num = random.randint(splitvalue,maxvalue)
	usedNum.append(num)
	bnum = bin(num)[2:]
	ckey["\t"] = bnum
	ckeyInv[bnum] = "\t"
	
	while (num in usedNum):
		num = random.randint(splitvalue,maxvalue)
	usedNum.append(num)
	bnum = bin(num)[2:]
	ckey["\n"] = bnum
	ckeyInv[bnum] = "\n"
	
	modCharList = charList.replace("\t","").replace("\n","")
	for i,c in enumerate(modCharList):
		while (num in usedNum):
			if (i<(splitvalue)):
				num = random.randint(0,(splitvalue-1))
			else:
				num = random.randint(splitvalue,maxvalue)
		usedNum.append(num)
		bnum = bin(num)[2:]
		while (len(bnum) < digits):
			bnum = "0" + bnum
		ckey[c] = bnum
		ckeyInv[bnum] = c

	key = random.randint((2**15),(2**60))
	return key, ckey, ckeyInv, splitSize

def xor(val,key):
	key = bin(key)[3:]
	i = 0

	newval = ""
	for v in val:
		if (v == key[i]):
			newval += "0"
		else:
			newval += "1"
		i += 1
		if (i == len(key)):
			key = bin(random.randint((2**15),(2**60)))[3:]
			i = 0

	return newval

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey):
	key, ckey, ckeyInv, splitSize = setKey(mainkey)

	tempText = ""
	for c in text:
		tempText += ckey[c]

	tempText = xor(tempText,key)

	digits = len(list(ckeyInv.keys())[0])-splitSize
	fillers = digits - len(tempText)%(digits)
	for i in range(fillers):#
		tempText = str(random.randint(0,1)) + tempText

	ctext = ""
	if (splitSize == 1):
		for i in range(digits,len(tempText)+1,digits):
			ctext += ckeyInv[("0" + tempText[i-digits:i])]
	elif (splitSize == 2):
		for i in range(digits,len(tempText)+1,digits):
			ctext += ckeyInv[("00" + tempText[i-digits:i])]
	else:
		print("Error splitSize")
		return "error", "error"

	return ctext, 1

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	key, ckey, ckeyInv, splitSize = setKey(mainkey)

	tempText = ""
	for c in ctext:
		tempText += ckey[c][splitSize:]

	digits = len(list(ckeyInv.keys())[0])
	fillers = len(tempText)%(digits)
	tempText = tempText[fillers:]#

	tempText = xor(tempText,key)

	text = ""
	for i in range(digits,len(tempText)+1,digits):
		text += ckeyInv[(tempText[i-digits:i])]#
	
	return text, 0