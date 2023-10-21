from tools import recTool as rt
from tools import tempGenerator as tg
import os
import json
import random
import importlib

def returnInfo(choice):

	infoLables = ["settingsType", "fileName"]

	info = [["General", "Cypher", "Hash", "RSA"],
		["generalSettings.json","cypherSettings.json","hashSettings.json","rsaSettings.json"]]

	return info[choice]

def returnSet(setType):
	fileNames = returnInfo(1)
	fileName = ""
	try:
		fileName = fileNames[setType]
	except:
		print("Error with selected setType: " + str(setType))
		return "error"

	pyloc = os.getcwd()
	fileloc = pyloc + "\\settings\\" + fileName

	settings = {}
	try:
		file_object = open(fileloc, 'r')
		settings = json.load(file_object)
		file_object.close()
	except:
		print("Error opening file: " + fileName)
		return "error"

	return settings

def edit(setType, settings):
	fileNames = returnInfo(1)
	fileName = ""
	try:
		fileName = fileNames[setType]
	except:
		print("Error with selected setType: " + str(setType))
		return "error"

	pyloc = os.getcwd()
	fileloc = pyloc + "\\settings\\" + fileName

	try:
		file_object = open(fileloc, 'w')
		json.dump(settings, file_object)
		file_object.close()
	except:
		print("Error opening file: " + fileName)
		return "error"
	return 1
	
def display(setType):
	settings = returnSet(setType)
	if settings == "error":
		return "error"
	
	print("\nSetting\t\t\tValue")
	print("----------------------------------------")
	for key in settings:
		if len(key) <= 6:
			print(key + " \t\t\t" + str(settings[key]))
		elif len(key) <= 14:
			print(key + " \t\t" + str(settings[key]))
		else:
			print(key + " \t" + str(settings[key]))

	return 1

def load():
	pyloc = os.getcwd()
	settings = returnSet(1)
	if (settings == "error"):
		return "error"
	fileloc = settings["locCypherList"]
	
	fileList = []
	try:
		fileList = os.listdir(fileloc)
	except:
		print("Error finding directory: " + fileloc)
		return "error"

	cypherFilesG = []
	cypherFilesI = []
	cypherFilesE = []
	importflag = True
	for file in fileList:
		if (file == "cypherTP.py" or file == "tempCypher.py" or file == "__init__.py"):
			continue
		elif (file == "rsa.py"):
			# if correct do something
			continue
		elif (file[-3:] == ".py"):
			working = True
			try:
				if (tg.createTempCypher(file[:-3]) == "error"):
					print("Error Functional Problem loading temp")
					working = False
				else:
					if (importflag):
						from cyphers import tempCypher as testCypher
						importflag = False
					else:
						importlib.reload(testCypher)

					flag = True
					if (type(testCypher.returnInfo(0)) != str):
						print("Error Name not str")
					else:
						print(testCypher.returnInfo(0))
					if (type(testCypher.returnInfo(1)) != str):
						print("Error Description not str")
					testKSIndicator = testCypher.returnInfo(2)
					if (type(testKSIndicator) != bool):
						print("Error Keep Size indicator (KSI) not boolean")
						working = False
						flag = False
					testMultiplyer = testCypher.returnInfo(3)
					if (type(testMultiplyer) != float and type(testMultiplyer) != int):
						print("Error Multiplyer not a Number")
						working = False
						flag = False
					elif (testMultiplyer < 1):
						print("Error unrealistic Multiplyer shoud be at least 1: " + testMultiplyer)
					elif (testKSIndicator and testMultiplyer != 1):
						print("Error Incorect Multiplyer for True KSI: " + testMultiplyer + " (should be 1)")
					inputRec = testCypher.returnInfo(4)
					outputRec = testCypher.returnInfo(5)
					i = 0
					while (flag and i < len(inputRec)):
						if (type(inputRec[i]) != float and type(inputRec[i]) != int):
							print("Error inputRec not a number")
							working = False
							flag = False
						elif (type(outputRec[i]) != float and type(outputRec[i]) != int):
							print("Error outputRec not a number")
							working = False
							flag = False
						else:

							testText = ""
							testInRec = rt.returnRec(inputRec[i])
							for _ in range(999):
								testText += testInRec[random.randint(0,len(testInRec)-1)]
							testKey = random.randint(999999,999999999999999)

							testcText, opo = testCypher.encrypt(testText, testKey)
							if (testText == testcText):
								print("Error ecrypt did not change text")
								working = False
								flag = False
							if (not rt.checkIfRec(testcText, outputRec[i])):
								print("Error Incorrect outputRec")
								working = False
								flag = False
							if (testKSIndicator and len(testText) != len(testcText)):
								print("Error does not keep size when indicated")
								working = False
								flag = False
							else:
								multiplyerDifferential = 1 - ((len(testText)*testMultiplyer)/len(testcText))
								margin = .1
								if ((not testKSIndicator) and abs(multiplyerDifferential) > margin):
									print("Error Multiplyer is outside of margin of error")
									working = False
									flag = False
							
							testOutput, opo = testCypher.decrypt(testcText, testKey)
							if (testText != testOutput):
								print("Error decrypt return to text")
								working = False
								flag = False							
						i += 1
			except:
				print("Error Functional Problem with cypher file")
				working = False
			if (working):
				if (file[:-3] in settings["inactiveList"]):
					cypherFilesI.append(file[:-3])
				else:
					cypherFilesG.append(file[:-3])
			else:
				cypherFilesE.append(file[:-3])
		else:
			continue

	settings["cypherList"] = cypherFilesG
	settings["inactiveList"] = cypherFilesI
	settings["errorList"] = cypherFilesE
	if (edit(1, settings) == "error"):
		return "error"
	elif (display(1) == "error"):
		return "error"
	else:
		return 1

def exportSet(epath, selected):
	typeNames = returnInfo(0)
	allSettings = {}
	for i,type in enumerate(typeNames):
		if (type in selected):
			temp = returnSet(i)
			if (temp == "error"):
				return "error"
			else:
				temp2 = temp.copy()
				for k in temp.keys():
					if (k not in selected[type]):
						del temp2[k]
				allSettings[type] = temp2
	
	pyloc = os.getcwd()
	try:
		os.chdir(epath)
	except:
		print("Error changing directory: " + epath)
		return "error"

	fileList = os.listdir()
	fileName = "AFESsettings"
	i = 1
	while ((fileName+str(i)+".json") in fileList):
		i += 1
	fileName = fileName + str(i) + ".json"
	
	try:
		file_object = open(fileName, 'w')
		json.dump(allSettings, file_object)
		file_object.close()
	except:
		print("Error opening file: " + fileName)
		return "error"
	
	try:
		os.chdir(pyloc)
	except:
		print("Error changing directory: " + fileloc)
		return "error"
	return 1

def importSet(ipathfile):
	allSettings = {}
	try:
		file_object = open(ipathfile, 'r')
		allSettings = json.load( file_object)
		file_object.close()
	except:
		print("Error opening file: " + ipathfile)
		return "error"

	typeNames = returnInfo(0)
	for type, settings in allSettings.items():
		try:
			i = typeNames.index(type)
			temp = returnSet(i)
			if (temp == "error"):
				print("Error pulling current settings: " + type)
				print("Continuing...")
			else:
				for key, value in settings.items():
					temp[key] = value
				if (edit(i, temp) == "error"):
					print("Error saving setting type: " + type)
					print("Continuing...")
				elif (display(i) == "error"):
					print("Error displaying setting type: " + type)
					print("Continuing...")
		except ValueError:
			print("Error finding setting type: " + type)
			print("Continuing...")
	return 1
