from tools import setManipulator as sm
import os

def createTempCypher(cypher):
	contents = ['''#temp file used to access other cypher files
from cyphers import ''',''' as cypher

def returnInfo(choice):
	return cypher.returnInfo(choice)

def encrypt(text, mainkey):
	return cypher.encrypt(text, mainkey)

def decrypt(ctext, mainkey):
	return cypher.decrypt(ctext, mainkey)''']

	pyloc = os.getcwd()
	settings = sm.returnSet(1)
	if (settings == "error"):
		return "error"
	fileloc = settings["locCypherList"]

	try:
		os.chdir(fileloc)
	except:
		print("Error changing directory: " + fileloc)
		return "error"

	try:
		content = contents[0] + cypher + contents[1]
		with open("tempCypher.py", 'w') as file_object:
			file_object.write(content)
	except:
		print("Error creating/changing tempCypher.py")
		return "error"

	try:
		os.chdir(pyloc)
	except:
		print("Error changing directory: " + pyloc)
		return "error"

	return 1