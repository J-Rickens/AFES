from tools import setManipulator as sm
import rsa
import os


def saveKeys(name, publicKey, privateKey):
	settings = sm.returnSet(3)
	if (settings == "error"):
		return settings

	if (settings["locPublic"][0] == "."):
		locPub = pyloc + settings["locPublic"][1:]
	else:
		locPub = settings["locPublic"]
	if (settings["locPrivate"][0] == "."):
		locPri = pyloc + settings["locPrivate"][1:]
	else:
		locPri = settings["locPrivate"]

	fileListPub = []
	try:
		fileListPub = os.listdir(locPub)
	except:
		print("Error pulling directory: " + locPub)
		return "error"
	fileListPri = []
	try:
		fileListPri = os.listdir(locPri)
	except:
		print("Error pulling directory: " + locPri)
		return "error"

	fileNamePub = "public_" + name
	fileNamePri = "private_" + name
	if (((fileNamePub+".pem") in fileListPub) or ((fileNamePri+".pem") in fileListPri)):
		fileNamePub += "_"
		fileNamePri += "_"
		i = 1
		while (((fileNamePub+str(i)+".pem") in fileListPub) or ((fileNamePri+str(i)+".pem") in fileListPri)):
			i += 1
		fileNamePub = fileNamePub + str(i) + ".pem"
		fileNamePri = fileNamePri + str(i) + ".pem"
	else:
		fileNamePub = fileNamePub + ".pem"
		fileNamePri = fileNamePri + ".pem"

	try:
		file_object = open((locPub+"\\"+fileNamePub), 'wb')
		file_object.write(publicKey.save_pkcs1("PEM"))
		file_object.close()
	except:
		print("Error opening file: " + fileNamePub)
		return "error"	
	try:
		file_object = open((locPri+"\\"+fileNamePri), 'wb')
		file_object.write(privateKey.save_pkcs1("PEM"))
		file_object.close()
	except:
		print("Error opening file: " + fileName)
		return "error"
	return fileNamePub, fileNamePri

def genKeys(name):
	settings = sm.returnSet(3)
	if (settings == "error"):
		return settings

	bitSize = settings["size"]
	publicKey, privateKey = rsa.newkeys(bitSize)

	return saveKeys(name, publicKey, privateKey)

def importKeys(name = "", needPub = True, needPri = True):
	pyloc = os.getcwd()
	settings = sm.returnSet(3)
	if (settings == "error"):
		return settings

	publicKey = ""
	if (needPub):
		if (settings["locPublic"][0] == "."):
			locPub = pyloc + settings["locPublic"][1:]
		else:
			locPub = settings["locPublic"]
		if (name == ""):
			fileListPub = []
			try:
				fileListPub = os.listdir(locPub)
			except:
				print("Error pulling directory: " + locPub)
			publicKey = []
			for fileName in fileListPub:
				if (len(fileName) >= 12 and fileName[-4:] == ".pem" and fileName[:7] == "public_"):
					try:
						file_object = open((locPub+"\\"+fileName), 'rb')
						publicKey.append(rsa.PublicKey.load_pkcs1(file_object.read()))
						file_object.close()
					except:
						print("Error opening key: " + fileName)
		else:
			try:
				file_object = open((locPub+"\\public_"+fileNamePub+".pem"), 'rb')
				publicKey = rsa.PublicKey.load_pkcs1(file_object.read())
				file_object.close()
			except:
				print("Error opening key: " + (locPub+"\\public_"+fileNamePub+".pem"))

	privateKey = ""
	if (needPri):
		if (settings["locPrivate"][0] == "."):
			locPri = pyloc + settings["locPrivate"][1:]
		else:
			locPri = settings["locPrivate"]
		if (name == ""):
			fileListPri = []
			try:
				fileListPri = os.listdir(locPri)
			except:
				print("Error pulling directory: " + locPri)
			privateKey = []
			for fileName in fileListPri:
				if (len(fileName) >= 13 and fileName[-4:] == ".pem" and fileName[:8] == "private_"):
					try:
						file_object = open((locPri+"\\"+fileName), 'rb')
						privateKey.append(rsa.PrivateKey.load_pkcs1(file_object.read()))
						file_object.close()
					except:
						print("Error opening key: " + fileName)
		else:
			try:
				file_object = open((locPri+"\\private_"+fileNamePri+".pem"), 'rb')
				privateKey = rsa.PrivateKey.load_pkcs1(file_object.read())
				file_object.close()
			except:
				print("Error opening key: " + (locPri+"\\private_"+fileNamePri+".pem"))

	if (len(publicKey) == 0 and len(privateKey) == 0):
		print("Error no keys found.")
		return "error"
	return publicKey, privateKey