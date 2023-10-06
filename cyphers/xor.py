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
		[0,0],
		[1,0]]

	return info[choice]

# potential error if len(charList) = 2**x+1
# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey):
	genSet = sm.returnSet(0)
	charList = genSet["charList"]
	random.seed(mainkey)

	digits = len(bin(len(charList)-1)[2:])
	splitvalue = 2**(digits-1)
	maxvalue = (2**digits)-1
	ckey = {}
	ckeyInv = {}
	usedNum = []

	num = random.randint(splitvalue,maxvalue)
	usedNum.append(num)
	num = bin(num)[2:]
	ckey["\t"] = num
	ckeyInv[num] = "\t"
	
	while (num in usedNum):
		num = random.randint(splitvalue,maxvalue)
	usedNum.append(num)
	num = bin(num)[2:]
	ckey["\n"] = num
	ckeyInv[num] = "\n"
	
	modCharList = charList.replace("\t","").replace("\n","")
	for i,c in enumerate(modCharList):
		while (num in usedNum):
			if (i<=(splitvalue+2)):
				num = random.randint(0,(splitvalue-1))
			else:
				num = random.randint(splitvalue,maxvalue)
		usedNum.append(num)
		num = bin(num)[2:]
		while (len(num) < digits):
			num = "0" + num
		ckey[c] = num
		ckeyInv[num] = c

	key = random.randint((2**15),(2**60))
	return key, ckey, ckeyInv, 1

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
	key, ckey, ckeyInv, opo = setKey(mainkey)

	tempText = ""
	for c in text:
		tempText += ckey[c]

	tempText = xor(tempText,key)

	digits = len(list(ckeyInv.keys())[0])-1
	fillers = digits - len(tempText)%(digits)
	for i in range(fillers):#
		tempText = str(random.randint(0,1)) + tempText#

	ctext = ""
	for i in range(digits,len(tempText)+1,digits)
		ctext += ckeyInv[("0"+tempText[i-digits:i])]

	return ctext, opo

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	key, ckey, ckeyInv, _ = setKey(mainkey)

	tempText = ""
	for c in ctext:
		tempText += ckey[c]

	digits = len(list(ckeyInv.keys())[0])
	fillers = (digits-1) - len(tempText)%(digits-1)
	tempText = tempText[fillers:]#

	tempText = xor(tempText,key)

	text = ""
	for i in range(digits,len(tempText)+1,digits)
		text += ckeyInv[(tempText[i-digits:i])]#
	
	return text, 0