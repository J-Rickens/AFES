import os
import json

def returnInfo(choice):

	infoLables = ["settingsType", "fileName"]

	info = [["General", "Cypher", "Hash", "RSA"],
		["generalSettings.json","cypherSettings.json","hashSettings.json","rsaSettings.json"]]

	return info[choice]

def display(setType):
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

def edit():
	return 1

def load():
	return 1

def exportSet(epath):
	return 1

def importSet(ipath):
	return 1