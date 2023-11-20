from tools import setManipulator as sm
from tools import tempGenerator as tg
from tools import recTool as rt
from tools import keyGenerator as rkg
from tools import encrypter as e
import os
import random
import importlib
import hashlib
import json
import codecs

def getStoredVals(cypherList, ctext, isPassword, RSAn = 1):
	mainkey = 0
	currentOpo = 0
	print("ctext:",ctext)

	genkey = 0
	random.seed(len(ctext))
	importFlag = True
	try:
		if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
			raise TempCypherError
		if (importFlag):
			from cyphers import tempCypher as cypher
			importFlag = False
		importlib.reload(cypher)

		while (cypher.returnInfo(3) > 1 or (0 not in cypher.returnInfo(4))):
			if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
				raise TempCypherError
			importlib.reload(cypher)

		if (not rt.checkIfRec("1234567890.",0)):
			print("Error numbers not in charList.")
			raise CharListError

		storedLen = e.getStoredLen()
		splitValue = random.randint(0,len(ctext)-1-storedLen)
		storedVal = cypher.decrypt(ctext[splitValue:splitValue+storedLen],len(ctext))[0]
		
		ctext = ctext[:splitValue] + ctext[splitValue+storedLen:]
		genkey = int(storedVal[:e.getGenkeyLen()])
		currentOpo = float(storedVal[e.getGenkeyLen():])
	except:
		print("Error running Cypher. layer: genkey")
		return "error"

	temp = e.mainkeyGen(isPassword, genkey, RSAn)
	print(temp)
	if (temp == "error"):
		print("Error mainkeyGen")
		return "error"
	else:
		mainkey = temp[0]
	return ctext, mainkey, currentOpo

def saveText(text, locSave = ""):
	hashSettings = sm.returnSet(2)
	if (hashSettings == "error"):
		return hashSettings
	storHash = hashlib.pbkdf2_hmac(hashSettings["typeSt"],text.encode(),codecs.decode(hashSettings["saltSt"], 'hex'),10000).hex()

	loc = ""
	fileName = ""
	if (locSave == ""):
		pyloc = os.getcwd()
		genSettings = sm.returnSet(0)
		if (genSettings == "error"):
			return genSettings
		if (genSettings["locSaveData"][0] == "."):
			loc = pyloc + genSettings["locSaveCypherText"][1:]
		else:
			loc = genSettings["locSaveCypherText"]
		fileName = "afesData.json"
		locSave = loc+"\\"+fileName
	else:
		locSave = locSave.split("\\")
		loc = "\\".join(locSave[:-1])
		fileName = locSave[-1]
		locSave = loc+"\\"+fileName

	data = {}
	try:
		if (fileName in os.listdir(loc)):
			file_object = open(locSave, 'r')
			data = json.load(file_object)
			file_object.close()
		else:
			data = {"Storage_Hash":"Data"}
	except:
		print("Error searching directory or loading current data file:", locSave)
		return "error"

	if (storHash in data):
		i = 0
		while ((storHash + "S" + str(i)) in data):
			i += 1
		storHash += "S" + str(i)
	data[storHash] = text

	try:
		file_object = open(locSave, 'w')
		json.dump(data, file_object)
		file_object.close()
	except:
		print("Error saving data file:", locSave)
		return "error"
	return locSave, storHash

def decrypt(ctext, layers = 3, sizeMulti = 0, locSave = "", isPassword = False, mainkey = "", currentOpo = 0):
	cypherSettings = sm.returnSet(1)
	if (cypherSettings == "error"):
		return cypherSettings
	cypherList = cypherSettings["cypherList"]

	if (mainkey == ""):
		temp = getStoredVals(cypherList, ctext, isPassword)
		if (temp == "error"):
			print("Error mainkeyGen")
			return "error"
		else:
			ctext = temp[0]
			mainkey = temp[1]
			currentOpo = temp[2]

	pickedCyphers = []
	importFlag = True
	currentMulti = 1
	for l in range(1,layers+1):
		layerKey = mainkey+(l**l)
		random.seed(layerKey)

		try:
			cypherSelect = random.randint(0,len(cypherList)-1)
			if (tg.createTempCypher(cypherList[cypherSelect]) == "error"):
				print("Error creating tempCypher")
				raise TempCypherError
			if (importFlag):
				from cyphers import tempCypher as cypher
				importFlag = False
			importlib.reload(cypher)
			recFlag = True # flag is inverted since it is used to keep while loop going
			for rec in cypher.returnInfo(4):
				if (rt.checkIfRec(rt.returnRec(currentOpo), rec)):
					recFlag = False
					break

			while (recFlag or (sizeMulti != 0 and ((currentMulti*cypher.returnInfo(3)) > sizeMulti)) ):
						cypherSelect = random.randint(0,len(cypherList)-1)
						if (tg.createTempCypher(cypherList[cypherSelect]) == "error"):
							print("Error creating tempCypher loop")
							raise TempCypherError
						importlib.reload(cypher)
						recFlag = True
						for rec in cypher.returnInfo(4):
							if (rt.checkIfRec(rt.returnRec(currentOpo), rec)):
								recFlag = False
								break
 
			for i, rec in enumerate(cypher.returnInfo(4)):
				if (rt.checkIfRec(rt.returnRec(currentOpo), rec)):
					currentOpo = cypher.returnInfo(5)[i]
					break
			currentMulti *= cypher.returnInfo(3)
			pickedCyphers.append(cypherSelect)
		except:
			print("Error finding Cypher. layer:",l)
			return "error"
	

	for c in pickedCyphers:
		print(cypherList[c])
	text = ctext
	for l in range(layers,0,-1):
		layerKey = mainkey+(l**l)
		random.seed(layerKey)

		try:
			if (tg.createTempCypher(cypherList[pickedCyphers[l-1]]) == "error"):
				print("Error creating tempCypher")
				raise TempCypherError
			importlib.reload(cypher)

			text, _ = cypher.decrypt(text, layerKey)

		except:
			print("Error running Cypher. layer:",l)
			return "error"

	tempSaver = saveText(text, locSave)
	if (tempSaver == "error"):
		print("Error in saveText.")
		return "error"
	else:
		return text, tempSaver[0], tempSaver[1]

def decryptWithRSA(ctext, privateKeyName, layers = 3, sizeMulti = 0, locSave = "", isPassword = False):
	tempRSAKeys = rkg.importKeys(name = privateKeyName, needPub = False)
	if (tempRSAKeys == "error"):
		print("Error running importKeys")
		return "error"
	privateKey = tempRSAKeys[1]

	text = ""
	try:
		for i in range(len(ctext)):
			ctext[i] = codecs.decode(ctext[i], 'hex')

		from cyphers import rsaCypher
		importlib.reload(rsaCypher)
		tempText = rsaCypher.decrypt(ctext, 0, privateKey)[0]
		for t in tempText:
			text += t
	except:
		print("Error running rsa cypher.")
		return "error"

	if (layers > 0):
		cypherSettings = sm.returnSet(1)
		if (cypherSettings == "error"):
			return cypherSettings
		cypherList = cypherSettings["cypherList"]

		temp = getStoredVals(cypherList, text, isPassword, privateKey.n)
		if (temp == "error"):
			print("Error mainkeyGen RSA")
			return "error"
		text = temp[0]
		mainkey = temp[1]
		currentOpo = temp[2]

		return decrypt(text, layers, sizeMulti, locSave, mainkey = mainkey, currentOpo = currentOpo)
	else:
		tempSaver = saveText(text, locSave)
		if (tempSaver == "error"):
			print("Error in saveText.")
			return "error"
		else:
			return text, tempSaver[0], tempSaver[1]