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

def encrypt(layers = 3, sizeMulti = 0, ctext, locSave = "", isPassword = False, isRSA = False, mainkey = "", genkey = 0):
	cypherSettings = sm.returnSet(1)
	if (cypherSettings == "error"):
		return cypherSettings
	cypherList = cypherSettings["cypherList"]

	currentOpo = 0
	for rec in rt.returnRec().keys():
		if (rt.checkIfRec(ctext, rec)):
			currentOpo = rec
	
	if (mainkey == ""):
		temp = e.mainkeyGen(isPassword)
		if (temp == "error"):
			print("Error mainkeyGen")
			return "error"
		else:
			genkey = temp[1]
			mainkey = temp[0]

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
			print("Error running Cypher. layer:",l)
			return "error"
