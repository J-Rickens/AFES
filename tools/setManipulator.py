from UI import UI
import os
import json

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

def edit():
	return 1

def load():
	pyloc = os.getwd()
	settings = returnSet(1)
	fileloc = settings["locCypherList"]
	try:
		os.chdir(fileloc)
	except:
		print("Error changing directory: " + fileloc)
		return "error"

	fileList = os.listdir()
	cypherFiles = []
	for file in fileList:
		if (file == "cypherTP.py"):
			continue
		elif (file == "rsa.py"):
			continue
		elif (file[-3:] == ".py"):
			cypherFiles.append(file)
		else:
			continue
	
	try:
		os.chdir(pyloc)
	except:
		print("Error changing directory: " + fileloc)
		return "error"
	return 1

def exportSet(epath):
	return 1

def importSet(ipath):
	return 1
