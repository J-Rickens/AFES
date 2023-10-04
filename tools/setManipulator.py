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

# still needs work: error messages, test string based on inputrec, check outputrec, and check rsa.py
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
					print("error")
				if (type(testCypher.returnInfo(1)) != str):
					print("error")
				if (type(testCypher.returnInfo(2)) != bool):
					print("error")
					working = False
					flag = False
				if (type(testCypher.returnInfo(3)) != float and type(testCypher.returnInfo(3)) != int):
					print("error")
					working = False
					flag = False
				inputRec = testCypher.returnInfo(4)
				outputRec = testCypher.returnInfo(5)
				i = 0
				while (flag or i < len(inputRec)):
					if (type(inputRec[i]) != float and type(inputRec[i]) != int):
						print("error")
						working = False
						flag = False
					elif (type(outputRec[i]) != float and type(outputRec[i]) != int):
						print("error")
						working = False
						flag = False
					else:
						testText = "asdf"# wright something to pick random string based on inputRec
						testKey = random.randint(999999,999999999999999)
						testcText = testCypher.encrypt(testText, testKey)
						# check if output matches output rec
						testOutput = testCypher.decypt(testcText, testKey)
						if (testText != testOutput or testText == testcText):
							print("error")
							working = False
							flag = False
					i += 1
			except:
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
