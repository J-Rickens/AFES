from tools import setManipulator as sm
from tools import tempGenerator as tg
from tools import recTool as rt
from tools import keyGenerator as rkg
import os
import random
import importlib
import hashlib
import json
import rsa

genkeySize = 16

def saveCtext(ctext, locSave = ""):
	hashSettings = sm.returnSet(2)
	if (hashSettings == "error"):
		return hashSettings

	locSave = locSave.split("\\")
	loc = "\\".join(locSave[:-1])
	fileName = locSave[-1]
	return 1

def mainkeyGen(isPassword = False, RSAn = 0):
	hashSettings = sm.returnSet(2)
	if (hashSettings == "error"):
		return hashSettings

	random.seed()
	genkey = random.randint(10**(genkeySize-1),(10**genkeySize)-1)

	phash = ""
	if (isPassowrd):
		hashFlag = True
		while (hashFlag):
			phash = int(hashlib.pbkdf2_hmac(hashSettings["typeEn"],input('Enter Password: ').encode(),hashSettings["saltEn"],10000).hex(), 16)
			if (phash == int(hashlib.pbkdf2_hmac(hashSettings["typeEn"],input('Re-enter Password: ').encode(),hashSettings["saltEn"],10000).hex(), 16)):
				hashFlag = False
			else:
				print("Password did not match. Please try again.")
		if (phash < 0):
			phash *= -1

	mainkey = (genkey + phash + RSAn)
	return mainkey, genkey

def encrypt(layers = 3, sizeMulti = 1, text = "", locText = "", locSave = "", isPassword = False, isRSA = False, mainkey = ""):
	if (sm.loadCyphers() == "error"):
		print("Error running loadCyphers.")
		return "error"
	cypherSettings = sm.returnSet(1)
	if (cypherSettings == "error"):
		return cypherSettings
	importFlag = True
	cypherList = []
	for c in cypherSettings["cypherList"]:
		if (tg.createTempCypher(c) == "error"):
			print("Error creating tempCypher:",c)
		else:
			if (importFlag):
				from cyphers import tempCypher as cypher
				importFlag = False
			else:
				importlib.reload(cypher)
			if (cypher.returnInfo(3) <= sizeMulti):
				cypherList.append(c)

	if (text == "" and locText == ""):
		print("Error no text.")
		return "error"
	elif (text == ""):
		try:
			file_object = open(locText, 'r')
			text = file_object.read()
			file_object.close()
			if (len(text) == 0):
				print("Error no text.")
				return "error"
		except:
			print("Error opening text:",locText)
			return "error"

	currentOpo = 0
	for rec in rt.returnRec("full").keys():
		if (rt.checkIfRec(text, rec)):
			currentOpo = rec
	
	genkey = 0
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
	for l in range(layers):
		layerKey = mainkey+((l+1)**l)
		random.seed(layerKey)
		try:
			if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
				raise TempCypherError
			if (importFlag):
				from cyphers import tempCypher as cypher
				importFlag = False
			importlib.reload(cypher)
			while ((currentMulti*cypher.returnInfo(3)) > sizeMulti or (not rt.checkIfRec(rt.returnRec(currentOpo), cypher.returnInfo(4)))):
				if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
					raise TempCypherError
				importlib.reload(cypher)
			
			ctext, currentOpo = cypher.encrypt(ctext, layerKey)
			currentMulti *= cypher.returnInfo(3)
		except:
			print("Error running Cypher. layer:",l)
			return "error"


	try:
		if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
			raise TempCypherError
		importlib.reload(cypher)
		while (cypher.returnInfo(3) > 1 or (0 not in cypher.returnInfo(4))):
			if (tg.createTempCypher(cypherList[random.randint(0,len(cypherList)-1)]) == "error"):
				raise TempCypherError
			importlib.reload(cypher)
		genkey = str(genkey)
		if (not rt.checkIfRec(genkey,0)):
			print("Error numbers not in charList.")
			raise CharListError

		splitValue = random.randint(0,len(ctext)-1)
		ctext = ctext[:splitValue] + cypher.encrypt(genkey,len(ctext)+len(genkey)) + ctext[splitValue:]
	except:
		print("Error running Cypher. layer: genkey")
			return "error"


	if (not isRSA):
		saveCtext(ctext, locSave)
	return ctext

def encryptWithRSA(layers = 3, text = "", locText = "", locSave = "", isPassword = False, publicKeyName = ""):
	if (publicKeyName == ""):
		publicKey, privateKey = rkg.importKeys(name = publicKeyName)
	else:
		publicKey, _ = rkg.importKeys(name = publicKeyName, needPri = False)

	mainkey = mainkeyGen(isPassword, True, publicKey.n)
	ctext = encrypt(layers, text, locText, isRSA = True, mainkey = mainkey)
	saveCtext(ctext, locSave)
	return ctext