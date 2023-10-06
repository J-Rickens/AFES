from tools import recTool as rt
import os
import json
import random

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
		with open(fileloc, 'r') as file_object:
			settings = json.load(file_object)
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
		with open(fileloc, 'w') as file_object:
			json.dump(settings, file_object)
	except:
		print("Error opening file: " + fileName)
		return "error"
	return 1
	
def display(setType):
	settings = returnSet(setType)
	
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
	pyloc = os.getwd()
	settings = returnSet(1)
	if (settings == "error"):
		return "error"
	fileloc = settings["locCypherList"]
	try:
		os.chdir(fileloc)
	except:
		print("Error changing directory: " + fileloc)
		return "error"

	fileList = os.listdir()
	cypherFilesG = []
	cypherFilesI = []
	cypherFilesE = []
	for file in fileList:
		if (file == "cypherTP.py"):
			continue
		elif (file == "rsa.py"):
			# if correct do something
			continue
		elif (file[-3:] == ".py"):
			working = True
			try:
				import file as testCypher

				flag = True
				if (type(testCypher.returnInfo(0)) != str):
					print("Error Name not str")
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
					print("Error Incorect Multiplyer for True KSI: " + testMultiplyer + " (should be 1)
				inputRec = testCypher.returnInfo(4)
				outputRec = testCypher.returnInfo(5)
				i = 0
				while (flag or i < len(inputRec)):
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
						testInRec = returnRec(inputRec[i])
						for i in range(999999):
							testText += testInRec[random.randint(0,len(testInRec)-1)]
						testKey = random.randint(999999,999999999999999)

						testcText = testCypher.encrypt(testText, testKey)
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
							multiplerDifferential = 1 - ((len(testText)*testMultiplyer)/len(testcText))
							margin = .1
							if ((not testKSIndicator) and abs(multiplyerDifferential) > margin):
								print("Error Multiplyer is outside of margin of error")
								working = False
								flag = False
						
						testOutput = testCypher.decypt(testcText, testKey)
						if (testText != testOutput):
							print("Error decrypt return to text")
							working = False
							flag = False							
					i += 1
			except:
				print("Error Functional Problem with cypher file")
				working = False
			if (working):
				if (file in settings[1]):
					cypherFilesI.append(file)
				else:
					cypherFilesG.append(file)
			else:
				cypherFilesE.append(file)
		else:
			continue
	try:
		os.chdir(pyloc)
	except:
		print("Error changing directory: " + fileloc)
		return "error"

	settings[0] = cypherFilesG
	settings[1] = cypherFilesI
	settings[2] = cypherFilesE
	if (edit(1, settings) == "error"):
		return "error"
	elif (display(1) == "error"):
		return "error"
	else:
		return 1

# edit to specify what to include (auto exclude personal data like filepath)
def exportSet(epath):
	typeNames = returnInfo(0)
	allSettings = {}
	for i,type in enumerate(typeNames):
		temp = returnSet(i)
		if (temp == "error"):
			return "error"
		else:
			allSettings[type] = temp
	
	pyloc = os.getwd()
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
		with open(fileName, 'w') as file_object:
			json.dump(allSettings, file_object)
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
		with open(ipathfile, 'r') as file_object:
			allSettings = json.load( file_object)
	except:
		print("Error opening file: " + ipathfile)
		return "error"

	typeNames = returnInfo(0)
	for type, settings in allSettings.items():
		try:
			i = typeNames.index(type)
			elif (edit(i, settings) == "error"):
				print("Error saving setting type: " + type)
				print("Continuing...")
			elif (display(i) == "error"):
				print("Error displaying setting type: " + type)
				print("Continuing...")
		except ValueError:
			print("Error finding setting type: " + type)
			print("Continuing...")
	return 1
