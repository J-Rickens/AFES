from tools import setManipulator as sm
import rsa
import os


def saveKeys(name, publicKey, privateKey):
	pyloc = os.getcwd()
	settings = sm.returnSet(3)
	if (settings == "error"):
		return settings

	if (settings["locPublic"][0] == "."):
		locPub = pyloc + settings["locPublic"][1:]
	else:
		locPub = settings["locPublic"]
	try:
		os.chdir(locPub)
	except:
		print("Error changing directory: " + locPub)
		return "error"

	fileList = os.listdir()
	fileName = "public_" + name
	if ((fileName+".pem") in fileList):
		fileName += "_"
		i = 1
		while ((fileName+str(i)+".pem") in fileList):
			i += 1
		fileName = fileName + str(i) + ".pem"
	else:
		fileName = fileName + ".pem"
	try:
		file_object = open(fileName, 'wb')
		file_object.write(publicKey.save_pkcs1("PEM"))
		file_object.close()
	except:
		print("Error opening file: " + fileName)
		return "error"


	if (settings["locPrivate"][0] == "."):
		locPri = pyloc + settings["locPrivate"][1:]
	else:
		locPri = settings["locPrivate"]
	try:
		os.chdir(locPri)
	except:
		print("Error changing directory: " + locPri)
		return "error"

	fileList = os.listdir()
	fileName = "private_" + name
	if ((fileName+".pem") in fileList):
		fileName += "_"
		i = 1
		while ((fileName+str(i)+".pem") in fileList):
			i += 1
		fileName = fileName + str(i) + ".pem"
	else:
		fileName = fileName + ".pem"
	try:
		file_object = open(fileName, 'wb')
		file_object.write(privateKey.save_pkcs1("PEM"))
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

def genKeys(name):
	settings = sm.returnSet(3)
	if (settings == "error"):
		return settings

	bitSize = settings["size"]
	publicKey, privateKey = rsa.newkeys(bitSize)

	if (saveKeys(name, publicKey, privateKey) == "error"):
		return "error"
	return 1