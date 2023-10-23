# Caesar Shift Cypher
from tools import setManipulator as sm
import random

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
def returnInfo(choice):

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["Caesar Shift Cypher",
		'''description''',
		True,
		1,
		[0, 1],
		[0, 1]]

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

	ckey = []
	for i in range(len(charList),0,-1):
		temp = random.randint(0,i-1)
		ckey.append(charList[temp])
		if temp+1 == len(charList):
			charList = charList[:temp]
		else:
			charList = charList[:temp] + charList[temp+1:]

	return ckey

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey, decrypting = False):
	check = False
	if (text.find("\t")==-1 and text.find("\n")==-1):
		check = True
	keyList = setKey(mainkey, True, check)
	key = random.randint(1-len(keyList),len(keyList)-1)
	while (key == 0):
		key = random.randint(1-len(keyList),len(keyList)-1)

	tkl = random.randint(4,10)
	kl = 0
	tk = random.randint(1,2)
	k = 0

	ctext = ""
	for char in text:
		tempk = random.randint(0,10)
		if tempk == 0 or kl == tkl:
			keyList = setKey(mainkey, False, check)
			tkl = random.randint(4,10)
			kl = 0
		if tempk%2 == 0 or k == tk:
			key = random.randint(1-len(keyList),len(keyList)-1)
			while (key == 0):
				key = random.randint(1-len(keyList),len(keyList)-1)
			tk = random.randint(1,2)
			k = 0

		if (decrypting):
			temp = keyList.index(char) - k + len(keyList)
		else:
			temp = keyList.index(char) + k + len(keyList)
		temp = temp % len(keyList)
		ctext += keyList[temp]

		kl += 1
		k += 1

	if check:
		return ctext, 1
	else:
		return ctext, 0

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	return encrypt(ctext, mainkey, True)