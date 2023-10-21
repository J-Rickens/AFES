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

	fileloc = fileloc + "\\tempCypher.py"
	content = contents[0] + cypher + contents[1]
	try:
		file_object = open(fileloc, 'w')
		file_object.write(content)
		file_object.close()
	except:
		print("Error creating/changing tempCypher.py")
		return "error"

	return 1