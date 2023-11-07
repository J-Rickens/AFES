from tools import setManipulator as sm
from tools import tempGenerator as tg
from tools import recTool as rt
from tools import keyGenerator as rkg
import os
import random
import importlib
import hashlib
import json
import codecs

genkeySize = 16

def saveCtext(ctext, locSave = "", isRSA = False):
	hashSettings = sm.returnSet(2)
	if (hashSettings == "error"):
		return hashSettings
	storHash = ""
	if (isRSA):
		storHash = hashlib.pbkdf2_hmac(hashSettings["typeSt"],ctext[0],codecs.decode(hashSettings["saltSt"], 'hex'),10000).hex()
	else:
		storHash = hashlib.pbkdf2_hmac(hashSettings["typeSt"],ctext.encode(),codecs.decode(hashSettings["saltSt"], 'hex'),10000).hex()

	loc = ""
	fileName = ""
	if (locSave == ""):
		pyloc = os.getcwd()
		genSettings = sm.returnSet(0)
		if (genSettings == "error"):
			return genSettings
		if (genSettings["locSaveCypherText"][0] == "."):
			loc = pyloc + genSettings["locSaveCypherText"][1:]
		else:
			loc = genSettings["locSaveCypherText"]
		fileName = "cypherText.json"
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
			data = {"Storage_Hash":"Cypher_Text"}
	except:
		print("Error searching directory or loading current data file:", locSave)
		return "error"

	if (storHash in data):
		i = 0
		while ((storHash + "S" + str(i)) in data):
			i += 1
		storHash += "S" + str(i)
	if (isRSA):
		for i in range(len(ctext)):
			ctext[i] = codecs.encode(ctext[i],'hex').decode()
	data[storHash] = ctext

	try:
		file_object = open(locSave, 'w')
		json.dump(data, file_object)
		file_object.close()
	except:
		print("Error saving data file:", locSave)
		return "error"
	return locSave, storHash

def mainkeyGen(isPassword = False, RSAn = 1):
	hashSettings = sm.returnSet(2)
	if (hashSettings == "error"):
		return hashSettings

	random.seed()
	genkey = random.randint(10**(genkeySize-1),(10**genkeySize)-3)

	phash = 1
	if (isPassword):
		hashFlag = True
		while (hashFlag):
			phash = int(hashlib.pbkdf2_hmac(hashSettings["typeEn"],input('Enter Password: ').encode(),codecs.decode(hashSettings["saltEn"], 'hex'),10000).hex(), 16)
			if (phash == int(hashlib.pbkdf2_hmac(hashSettings["typeEn"],input('Re-enter Password: ').encode(),codecs.decode(hashSettings["saltEn"], 'hex'),10000).hex(), 16)):
				hashFlag = False
			else:
				print("Password did not match. Please try again.")
		if (phash < 0):
			phash *= -1

	mainkey = (genkey + phash + RSAn)%(10**(genkeySize*4))
	return mainkey, genkey

def encrypt(layers = 3, sizeMulti = 0, text = "", locText = "", locSave = "", isPassword = False, isRSA = False, mainkey = "", genkey = 0):
	cypherSettings = sm.returnSet(1)
	if (cypherSettings == "error"):
		return cypherSettings
	cypherList = []
	cypherList = cypherSettings["cypherList"]
	'''if (sizeMulti == 0):
		cypherList = cypherSettings["cypherList"]
	else:
		if (tg.createTempCypher(cypherSettings["cypherList"][0]) == "error"):
			print("Error creating tempCypher:",cypherSettings["cypherList"][0])
			return "error"
		from cyphers import tempCypher as cypher
		for c in cypherSettings["cypherList"]:
			if (tg.createTempCypher(c) == "error"):
				print("Error creating tempCypher:",c)
			else:
				importlib.reload(cypher)
				if (cypher.returnInfo(3) <= sizeMulti):
					cypherList.append(c)
	print(cypherList)'''

	if (text == "" and locText == ""):
		print("Error no text.")
		return "error"
	elif (text == ""):
		try:
			file_object = open(locText, 'r')
			text = file_object.read()
			file_object.close()
			if (len(text) == 0):
				print("Error no text in file.")
				return "error"
		except:
			print("Error opening text:",locText)
			return "error"

	currentOpo = 0
	for rec in rt.returnRec().keys():
		if (rt.checkIfRec(text, rec)):
			currentOpo = rec
	
	if (mainkey == ""):
		temp = mainkeyGen(isPassword)
		if (temp == "error"):
			print("Error mainkeyGen")
			return "error"
		else:
			genkey = temp[1]
			mainkey = temp[0]

	
	importFlag = True
	ctext = text
	currentMulti = 1
	for l in range(1,layers+1):
		layerKey = mainkey+(l**l)
		random.seed(layerKey)

		try:
			if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
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
				if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
					print("Error creating tempCypher loop")
					raise TempCypherError
				importlib.reload(cypher)
				recFlag = True
				for rec in cypher.returnInfo(4):
					if (rt.checkIfRec(rt.returnRec(currentOpo), rec)):
						recFlag = False
						break

			ctext, currentOpo = cypher.encrypt(ctext, layerKey)
			currentMulti *= cypher.returnInfo(3)
		except:
			print("Error running Cypher. layer:",l)
			return "error"


	importFlag = True
	try:
		if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
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

		while (cypher.returnInfo(3) > 1 or (0 not in cypher.returnInfo(4))):
			if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
				raise TempCypherError
			importlib.reload(cypher)
			recFlag = True
			for rec in cypher.returnInfo(4):
				if (rt.checkIfRec(rt.returnRec(currentOpo), rec)):
					recFlag = False
					break

		genkey = str(genkey)
		if (not rt.checkIfRec(genkey,0)):
			print("Error numbers not in charList.")
			raise CharListError

		splitValue = random.randint(0,len(ctext)-1)
		ctext = ctext[:splitValue] + cypher.encrypt(genkey,len(ctext)+len(genkey))[0] + ctext[splitValue:]
	except:
		print("Error running Cypher. layer: genkey")
		return "error"


	if (not isRSA):
		tempSaver = saveCtext(ctext, locSave)
		if (tempSaver == "error"):
			print("Error in saveCtext.")
			return "error"
		else:
			return ctext, tempSaver[0], tempSaver[1]
	else:
		return ctext

def encryptWithRSA(layers = 3, sizeMulti = 0, text = "", locText = "", locSave = "", isPassword = False, publicKeyName = ""):
	if (text == "" and locText == ""):
		print("Error no text.")
		return "error"
	elif (text == ""):
		try:
			file_object = open(locText, 'r')
			text = file_object.read()
			file_object.close()
			if (len(text) == 0):
				print("Error no text in file.")
				return "error"
		except:
			print("Error opening text:",locText)
			return "error"

	publicKey = ""
	tempRSAKeys = rkg.importKeys(name = publicKeyName)
	if (tempRSAKeys == "error"):
		print("Error running importKeys")
		return "error"
	elif (publicKeyName == ""):
		for key in tempRSAKeys[1].keys():
			if (key in tempRSAKeys[0]):
				publicKey = tempRSAKeys[0][key]
				break
	else:
		publicKey = tempRSAKeys[0]

	mainkey = 0
	genkey = 0
	tempkeys = mainkeyGen(isPassword, publicKey.n)
	if (tempkeys == "error"):
		print("Error mainkeyGen")
		return "error"
	else:
		mainkey = tempkeys[0]
		genkey = tempkeys[1]


	ctext = encrypt(layers = layers, sizeMulti = sizeMulti, text = text, isRSA = True, mainkey = mainkey, genkey = genkey)
	if (ctext == "error"):
		print("Error in regular encrypt.")
		return "error"

	try:
		from cyphers import rsaCypher
		importlib.reload(rsaCypher)
		ctext = rsaCypher.encrypt(ctext, mainkey, publicKey)[0]
	except:
		print("Error running rsa cypher.")
		return "error"


	tempSaver = saveCtext(ctext, locSave, True)
	if (tempSaver == "error"):
		print("Error in saveCtext.")
		return "error"
	else:
		return ctext, tempSaver[0], tempSaver[1]