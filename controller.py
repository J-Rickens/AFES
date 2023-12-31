from tools import setManipulator as sm
from tools import keyGenerator as rkg
from tools import encrypter as e
from tools import decrypter as d
from UI import UI as ui
import os
import hashlib
import codecs
import json

def textMenu():
	while (True):
		textChoice = ui.menu('''\nEnter a number from the text menu
				\n0: Back
				\n1: Exit
				\n2: Type Text
				\n3: Chose file
				\n''')
	
		if (textChoice == 0):
			return 0, 0
		elif (textChoice == 1):
			return 1, 1
		elif (textChoice == 2):
			return 2, input("Enter Text:\n")
		elif (textChoice == 3):
			loc = ui.getLoc()
			if (loc == 1):
				return 1, 1
			elif (loc == 0):
				continue
			else:
				return 3, loc

def RSAkeyMenu(isPub):
	pubkeys, prikeys = rkg.importKeys()
	menuStr = '''\nEnter a number from the menu
			\n0: Back
			\n1: Exit
			\n'''
	if (isPub):
		menuStr += "2: New Key\n"
		for i, key in enumerate(pubkeys):
			menuStr += str(i+3) + ": public_" + key + "\n"
	else:
		for i, key in enumerate(prikeys):
			menuStr += str(i+2) + ": private_" + key + "\n"
	
	RSAChoice = ui.menu(menuStr)
	if (RSAChoice == 0 or RSAChoice == 1):
		return RSAChoice
	elif (isPub and RSAChoice == 2):
		return rkg.genKeys("key")[0][7:-4]
	else:
		menuNumList = menuStr.split('\n')# split by menu option
		for id, line in enumerate(menuNumList):# determin valid number options
			menuNumList[id] = line.split(':')
			if (menuNumList[id][0].isdigit() and int(menuNumList[id][0]) == RSAChoice):
				if (isPub):
					return menuNumList[id][1][8:]
				else:
					return menuNumList[id][1][9:]



def encrypterMenu():
	while (True):
		choice = ui.menu('''\nEnter a number from the encrypter menu
				\n0: Back
				\n1: Exit
				\n2: Default Encrypt
				\n3: Quick Encrypt
				\n4: Long Encrypt
				\n5: Encrypt with just RSA
				\n6: Default Encrypt with RSA
				\n7: Quick Encrypt with RSA
				\n8: Long Encrypt with RSA
				\n9: Custom Encrypt
				\n10: Define Default, Quick, and Long settings
				\n''')
	
		if (choice == 0):# Back to main menu
			return 0
		elif (choice == 1):# Exit
			return 1
		elif (choice == 10):# Display info on settings
			displayChoice = ui.menu('''\nEnter a 0 or 1 from the menu
					\n0: Back
					\n1: Exit
					\nDefault: isPassword=True, layers=3, sizeMultiplyer=0
					\nQuick: isPassword=False, layers=2, sizeMultiplyer=1
					\nLong: isPassword=True, layers=5, sizeMultiplyer=0
					\n''')
			if (displayChoice == 1):
				return 1
			elif (displayChoice == 0):
				continue
		
		textChoice, text = textMenu()
		if (textChoice == 1):# Exit
			return 1
		elif (textChoice == 0):# Back to Encrypter Menu
			continue
		elif (choice == 2):# Default encryption
			if (textChoice == 2):
				e.encrypt(text = text, isPassword = True)
			elif (textChoice == 3):
				e.encrypt(locText = text, isPassword = True)
			else:
				print("Error choice selection: textChoice",textChoice)
		elif (choice == 3):# quick encyption
			if (textChoice == 2):
				e.encrypt(layers = 2, sizeMulti = 1, text = text)
			elif (textChoice == 3):
				e.encrypt(layers = 2, sizeMulti = 1, locText = text)
			else:
				print("Error choice selection: textChoice",textChoice)
		elif (choice == 4):# long encyption
			if (textChoice == 2):
				e.encrypt(layers = 5, text = text, isPassword = True)
			elif (textChoice == 3):
				e.encrypt(layers = 5, locText = text, isPassword = True)
			else:
				print("Error choice selection: textChoice",textChoice)

		elif (choice == 9):# custom encryption settings
			customizerMenuNum = 1
			flag = False
			while (True):
				if (customizerMenuNum == 1):
					isPassword = False
					custChoice = ui.menu('''\nEnter a number from the customizer menu 1/5
							\n0: Back
							\n1: Exit
							\n2: Use Password
							\n3: Don't use Password
							\n''')
					if (custChoice == 1):
						return 1
					elif (custChoice == 0):
						break
					elif (custChoice == 2):
						isPassword = True
						customizerMenuNum = 2
					elif (custChoice == 3):
						isPassword = False
						customizerMenuNum = 2

				elif (customizerMenuNum == 2):
					isRSA = False
					layerMin = 1
					custChoice = ui.menu('''\nEnter a number from the customizer menu 2/5
							\n0: Back
							\n1: Exit
							\n2: Use RSA
							\n3: Don't use RSA
							\n''')
					if (custChoice == 1):
						return 1
					elif (custChoice == 0):
						customizerMenuNum = 1
					elif (custChoice == 2):
						isRSA = True
						customizerMenuNum = 2.5
					elif (custChoice == 3):
						isRSA = False
						customizerMenuNum = 3

				elif (customizerMenuNum == 2.5):
					layerMin = 0
					pubkey = RSAkeyMenu(True)
					if (pubkey == 1):
						return 1
					elif (pubkey == 0):
						customizerMenuNum = 2
					else:
						customizerMenuNum = 3

				elif (customizerMenuNum == 3):
					layers = ui.getNum('''How many Layers 
							\n(Enter "back" or "exit" to go back or exit) customizer menu 3/5:
							\n''', min = layerMin, max = 10)
					if (layers == "exit"):
						return 1
					elif (layers == "back"):
						customizerMenuNum = 2
					else:
						customizerMenuNum = 4

				elif (customizerMenuNum == 4):
					sizeMulti = ui.getNum('''How many times bigger can the text be (Enter 0 for no limit)
							\n(Enter "back" or "exit" to go back or exit) customizer menu 4/5:
							\n''', min = 0, isInt = False)
					if (sizeMulti == "exit"):
						return 1
					elif (sizeMulti == "back"):
						customizerMenuNum = 3
					else:
						customizerMenuNum = 5

				elif (customizerMenuNum == 5):
					locSave = ""
					custChoice = ui.menu('''\nEnter a number from the customizer menu 5/5
							\n0: Back
							\n1: Exit
							\n2: Use Default Save Location
							\n3: Enter a Save Location
							\n''')
					if (custChoice == 1):
						return 1
					elif (custChoice == 0):
						customizerMenuNum = 4
					elif (custChoice == 2):
						break
					elif (custChoice == 3):
						customizerMenuNum = 5.5

				elif (customizerMenuNum == 5.5):
					locSave = ui.getLoc(isExist = False)
					if (locSave == 1):
						return 1
					elif (locSave == 0):
						customizerMenuNum = 5
					else:
						break

			if (customizerMenuNum == 1):
				continue
			elif (isRSA):
				if (textChoice == 2):
					e.encryptWithRSA(layers = layers, sizeMulti = sizeMulti, text = text, locSave = locSave, isPassword = isPassword, publicKeyName = pubkey)
				elif (textChoice == 3):
					e.encryptWithRSA(layers = layers, sizeMulti = sizeMulti, locText = text, locSave = locSave, isPassword = isPassword, publicKeyName = pubkey)
				else:
					print("Error choice selection: textChoice",textChoice)
			else:
				if (textChoice == 2):
					e.encrypt(layers = layers, sizeMulti = sizeMulti, text = text, locSave = locSave, isPassword = isPassword)
				elif (textChoice == 3):
					e.encrypt(layers = layers, sizeMulti = sizeMulti, locText = text, locSave = locSave, isPassword = isPassword)
				else:
					print("Error choice selection: textChoice",textChoice)

		else:
			pubkey = RSAkeyMenu(True)
			if (pubkey == 1):
				return 1
			elif (pubkey == 0):
				continue
			elif (choice == 5):# just RSA encyption
				if (textChoice == 2):
					e.encryptWithRSA(layers = 0, text = text, publicKeyName = pubkey)
				elif (textChoice == 3):
					e.encryptWithRSA(layers = 0, locText = text, publicKeyName = pubkey)
				else:
					print("Error choice selection: textChoice",textChoice)
			elif (choice == 6):# Default encryption with RSA
				if (textChoice == 2):
					e.encryptWithRSA(text = text, isPassword = True, publicKeyName = pubkey)
				elif (textChoice == 3):
					e.encryptWithRSA(locText = text, isPassword = True, publicKeyName = pubkey)
				else:
					print("Error choice selection: textChoice",textChoice)
			elif (choice == 7):# quick encyption with RSA
				if (textChoice == 2):
					e.encryptWithRSA(layers = 2, sizeMulti = 1, text = text, publicKeyName = pubkey)
				elif (textChoice == 3):
					e.encryptWithRSA(layers = 2, sizeMulti = 1, locText = text, publicKeyName = pubkey)
				else:
					print("Error choice selection: textChoice",textChoice)
			elif (choice == 8):# long encyption with RSA
				if (textChoice == 2):
					e.encryptWithRSA(layers = 5, text = text, isPassword = True, publicKeyName = pubkey)
				elif (textChoice == 3):
					e.encryptWithRSA(layers = 5, locText = text, isPassword = True, publicKeyName = pubkey)
				else:
					print("Error choice selection: textChoice",textChoice)

def ctextMenu():
	loc = ""
	pyloc = os.getcwd()
	genSettings = sm.returnSet(0)
	if (genSettings == "error"):
		return 0
	if (genSettings["locSaveCypherText"][0] == "."):
		loc = pyloc + genSettings["locSaveCypherText"][1:]
	else:
		loc = genSettings["locSaveCypherText"]
	if (loc[-1] != '\\'):
		loc += '\\'

	menuStrFile = '''\nEnter a number from the file list menu
			\n0: Back
			\n1: Exit
			\n'''
	fileList = []
	try:
		fileList = os.listdir(loc)
	except:
		print("Error pulling filelist:", loc)
		return 0
	temp = []
	i = 2
	for file in fileList:
		if (file[-5:] == ".json"):
			temp.append(file)
			menuStrFile += str(i) + ": " + file + "\n"
			i += 1
	fileList = temp

	while (True):
		choice = ui.menu(menuStrFile)
		if (choice == 1):
			return 1
		elif (choice == 0):
			return 0
		else:
			menuStr = '''\nEnter a number from the hash list menu
					\n0: Back
					\n1: Exit
					\n'''
			fileData = {}
			try:
				file_object = open((loc+fileList[choice-2]), 'r')
				fileData = json.load(file_object)
				file_object.close()
			except:
				print("Error pulling fileData:", (loc+fileList[choice-2]))
				continue
			hashList = []
			i = 2
			try:
				if (fileData["Storage_Hash"] != "Cypher_Text"):
					raise InvalidDataError
				for key in fileData.keys():
					if (key != "Storage_Hash"):
						hashList.append(key)
						menuStr += str(i) + ": " + key + "\n"
						i += 1
			except:
				print("Error using fileData:", (loc+fileList[choice-2]))
				continue

			choice = ui.menu(menuStr)
			if (choice == 1):
				return 1
			elif (choice == 0):
				continue
			else:
				return fileData[hashList[choice-2]]

def decrypterMenu():
	while (True):
		choice = ui.menu('''\nEnter a number from the decrypter menu
				\n0: Back
				\n1: Exit
				\n2: Default Decrypt
				\n3: Quick Decrypt
				\n4: Long Decrypt
				\n5: Decrypt with just RSA
				\n6: Default Decrypt with RSA
				\n7: Quick Decrypt with RSA
				\n8: Long Decrypt with RSA
				\n9: Custom Decrypt
				\n10: Define Default, Quick, and Long settings
				\n''')

		if (choice == 0):# Back to main menu
			return 0
		elif (choice == 1):# Exit
			return 1
		elif (choice == 10):# Display info on settings
			displayChoice = ui.menu('''\nEnter a 0 or 1 from the menu
					\n0: Back
					\n1: Exit
					\nDefault: isPassword=True, layers=3, sizeMultiplyer=0
					\nQuick: isPassword=False, layers=2, sizeMultiplyer=1
					\nLong: isPassword=True, layers=5, sizeMultiplyer=0
					\n''')
			if (displayChoice == 1):
				return 1
			elif (displayChoice == 0):
				continue

		ctext = ctextMenu()
		if (ctext == 1):# Exit
			return 1
		elif (ctext == 0):# Back to Decrypter Menu
			continue
		elif (choice == 2):# Default decryption
			d.decrypt(ctext, isPassword = True)
		elif (choice == 3):# quick decyption
			d.decrypt(ctext, layers = 2, sizeMulti = 1)
		elif (choice == 4):# long decyption
			d.decrypt(ctext, layers = 5, isPassword = True)

		elif (choice == 9):# custom decryption settings
			customizerMenuNum = 1
			flag = False
			while (True):
				if (customizerMenuNum == 1):
					isPassword = False
					custChoice = ui.menu('''\nEnter a number from the customizer menu 1/5
							\n0: Back
							\n1: Exit
							\n2: Use Password
							\n3: Don't use Password
							\n''')
					if (custChoice == 1):
						return 1
					elif (custChoice == 0):
						break
					elif (custChoice == 2):
						isPassword = True
						customizerMenuNum = 2
					elif (custChoice == 3):
						isPassword = False
						customizerMenuNum = 2

				elif (customizerMenuNum == 2):
					isRSA = False
					layerMin = 1
					custChoice = ui.menu('''\nEnter a number from the customizer menu 2/5
							\n0: Back
							\n1: Exit
							\n2: Use RSA
							\n3: Don't use RSA
							\n''')
					if (custChoice == 1):
						return 1
					elif (custChoice == 0):
						customizerMenuNum = 1
					elif (custChoice == 2):
						isRSA = True
						customizerMenuNum = 2.5
					elif (custChoice == 3):
						isRSA = False
						customizerMenuNum = 3

				elif (customizerMenuNum == 2.5):
					layerMin = 0
					prikey = RSAkeyMenu(False)
					if (prikey == 1):
						return 1
					elif (prikey == 0):
						customizerMenuNum = 2
					else:
						customizerMenuNum = 3

				elif (customizerMenuNum == 3):
					layers = ui.getNum('''How many Layers 
							\n(Enter "back" or "exit" to go back or exit) customizer menu 3/5:
							\n''', min = layerMin, max = 10)
					if (layers == "exit"):
						return 1
					elif (layers == "back"):
						customizerMenuNum = 2
					else:
						customizerMenuNum = 4

				elif (customizerMenuNum == 4):
					sizeMulti = ui.getNum('''How many times bigger can the text be (Enter 0 for no limit)
							\n(Enter "back" or "exit" to go back or exit) customizer menu 4/5:
							\n''', min = 0, isInt = False)
					if (sizeMulti == "exit"):
						return 1
					elif (sizeMulti == "back"):
						customizerMenuNum = 3
					else:
						customizerMenuNum = 5

				elif (customizerMenuNum == 5):
					locSave = ""
					custChoice = ui.menu('''\nEnter a number from the customizer menu 5/5
							\n0: Back
							\n1: Exit
							\n2: Use Default Save Location
							\n3: Enter a Save Location
							\n''')
					if (custChoice == 1):
						return 1
					elif (custChoice == 0):
						customizerMenuNum = 4
					elif (custChoice == 2):
						break
					elif (custChoice == 3):
						customizerMenuNum = 5.5

				elif (customizerMenuNum == 5.5):
					locSave = ui.getLoc(isExist = False)
					if (locSave == 1):
						return 1
					elif (locSave == 0):
						customizerMenuNum = 5
					else:
						break

			if (customizerMenuNum == 1):
				continue
			elif (isRSA):
				d.decryptWithRSA(ctext, prikey, layers = layers, sizeMulti = sizeMulti, locSave = locSave, isPassword = isPassword)
			else:
				d.decrypt(ctext, layers = layers, sizeMulti = sizeMulti, locSave = locSave, isPassword = isPassword)

		else:
			prikey = RSAkeyMenu(False)
			if (prikey == 1):
				return 1
			elif (prikey == 0):
				continue
			elif (choice == 5):# just RSA encyption
				d.decryptWithRSA(ctext, prikey, layers = 0)
			elif (choice == 6):# Default encryption with RSA
				d.decryptWithRSA(ctext, prikey, isPassword = True)
			elif (choice == 7):# quick encyption with RSA
				d.decryptWithRSA(ctext, prikey, layers = 2, sizeMulti = 1)
			elif (choice == 8):# long encyption with RSA
				d.decryptWithRSA(ctext, prikey, layers = 5, isPassword = True)

def rsaMenu():
	while (True):
		choice = ui.menu('''\nEnter a number from the Settings menu
				\n0: Back
				\n1: Exit
				\n2: Display Keys
				\n3: Make new Keys
				\n''')
		
		if (choice == 0):
			return 0
		elif (choice == 1):
			return 1
		elif (choice == 2):
			pubkeys, prikeys = rkg.importKeys()
			menuStr = '''\nEnter a number from the menu
				\n0: Back
				\n1: Exit
				\n'''
			for key in pubkeys:
				menuStr += "public_" + key + "\n"
			for key in prikeys:
				menuStr += "private_" + key + "\n"
			if (1 == ui.menu(menuStr)):
				return 1
		elif (choice == 3):
			name = input("Enter the key names: ")
			rkg.genKeys(name)

def setCategoryMenu(prompt = "", isAll = True):
	setList = sm.returnInfo(0)
	menuList = "\nEnter a number from the Settings Category " + prompt + '''menu
			\n0: Back
			\n1: Exit
			\n'''
	shift = 2
	if (isAll):
		menuList += "2: All\n"
		shift += 1
	for i, set in enumerate(setList):
		menuList += str(i+shift) + ": " + set + "\n"

	return ui.menu(menuList)

def editSetMenu(setType, itemType):
	if (setType == 0):# setType General
		settings = sm.returnSet(setType)
		if (list(settings.keys())[itemType] == "locExport"):
			loc = ui.getLoc(isJustPath = True)
			if (loc == 1):
				return 1
			elif (loc == 0):
				return 0
			else:
				settings["locExport"] = loc
				sm.edit(setType, settings)
				return 0

		elif (list(settings.keys())[itemType] == "locSaveData"):
			loc = ui.getLoc(isJustPath = True)
			if (loc == 1):
				return 1
			elif (loc == 0):
				return 0
			else:
				settings["locSaveData"] = loc
				sm.edit(setType, settings)
				return 0

		elif (list(settings.keys())[itemType] == "locSaveCypherText"):
			loc = ui.getLoc(isJustPath = True)
			if (loc == 1):
				return 1
			elif (loc == 0):
				return 0
			else:
				settings["locSaveCypherText"] = loc
				sm.edit(setType, settings)
				return 0
		else:
			print("Setting is not eligible for editting.")
			return 0

	elif (setType == 1):# setType Cypher
		settings = sm.returnSet(setType)
		if (list(settings.keys())[itemType] == "locCypherList"):
			loc = ui.getLoc(isJustPath = True)
			if (loc == 1):
				return 1
			elif (loc == 0):
				return 0
			else:
				settings["locCypherList"] = loc
				sm.edit(setType, settings)
				return 0
		else:
			print("Setting is not eligible for editting.")
			return 0

	elif (setType == 2):# setType Hash
		settings = sm.returnSet(setType)
		if (list(settings.keys())[itemType] == "typeEn"):
			menuStr = '''\nEnter a number from the Hash Type menu
					\n0: Back
					\n1: Exit
					\n'''
			typeList = []
			for i, type in enumerate(hashlib.algorithms_available):
				menuStr += str(i+2) + ": " + type + "\n"
				typeList.append(type)
			choice = ui.menu(menuStr)
			if (choice == 1):
				return 1
			elif (choice == 0):
				return 0
			else:
				settings["typeEn"] = typeList[choice-2]
				sm.edit(setType, settings)
				return 0

		elif (list(settings.keys())[itemType] == "sizeEn"):
			size = ui.getNum('''Password salt size (Enter "back" or "exit" to go back or exit):
							\n''', min = 16, max = 128)
			if (size == "exit"):
				return 1
			elif (size == "back"):
				return 0
			else:
				settings["sizeEn"] = size
				sm.edit(setType, settings)
				return 0

		elif (list(settings.keys())[itemType] == "saltEn"):
			settings['saltEn'] = codecs.encode(os.urandom(settings['sizeEn']),'hex').decode()
			sm.edit(setType, settings)
			return 0

		elif (list(settings.keys())[itemType] == "typeSt"):
			menuStr = '''\nEnter a number from the Hash Type menu
					\n0: Back
					\n1: Exit
					\n'''
			typeList = []
			for i, type in enumerate(hashlib.algorithms_available):
				menuStr += str(i+2) + ": " + type + "\n"
				typeList.append(type)
			choice = ui.menu(menuStr)
			if (choice == 1):
				return 1
			elif (choice == 0):
				return 0
			else:
				settings["typeSt"] = typeList[choice-2]
				sm.edit(setType, settings)
				return 0

		elif (list(settings.keys())[itemType] == "sizeSt"):
			size = ui.getNum('''Storage salt size (Enter "back" or "exit" to go back or exit):
							\n''', min = 8, max = 128)
			if (size == "exit"):
				return 1
			elif (size == "back"):
				return 0
			else:
				settings["sizeSt"] = size
				sm.edit(setType, settings)
				return 0

		elif (list(settings.keys())[itemType] == "saltSt"):
			settings['saltSt'] = codecs.encode(os.urandom(settings['sizeSt']),'hex').decode()
			sm.edit(setType, settings)
			return 0
		else:
			print("Setting is not eligible for editting.")
			return 0

	elif (setType == 3):# setType RSA
		settings = sm.returnSet(setType)
		if (list(settings.keys())[itemType] == "size"):
			size = ui.getNum('''RSA Key Size in bytes (Enter "back" or "exit" to go back or exit):
							\n''', min = 512, max = 4096)
			if (size == "exit"):
				return 1
			elif (size == "back"):
				return 0
			else:
				settings["size"] = size
				sm.edit(setType, settings)
				return 0

		elif (list(settings.keys())[itemType] == "locPublic"):
			loc = ui.getLoc(isJustPath = True)
			if (loc == 1):
				return 1
			elif (loc == 0):
				return 0
			else:
				settings["locPublic"] = loc
				sm.edit(setType, settings)
				return 0

		elif (list(settings.keys())[itemType] == "locPrivate"):
			loc = ui.getLoc(isJustPath = True)
			if (loc == 1):
				return 1
			elif (loc == 0):
				return 0
			else:
				settings["locPrivate"] = loc
				sm.edit(setType, settings)
				return 0
		else:
			print("Setting is not eligible for editting.")
			return 0

	else:
		print("Error setting type not defined:", setType)
		return 0


def setItemMenu(setType, isEdit = False):
	settingItems = sm.returnSet(setType)
	menuStr = '''\nEnter a number from the Settings Item menu
			\n0: Back
			\n1: Exit
			\n'''
	for i, key in enumerate(settingItems.keys()):
		menuStr += str(i+2) + ": " + key + " -> " + str(settingItems[key]) + "\n"

	setChoice = ui.menu(menuStr)
	if (setChoice == 1):
		return 1
	elif (setChoice == 0):
		return 0
	else:
		if (isEdit):
			return editSetMenu(setType, setChoice-2)
		else:
			typeNames = sm.returnInfo(0)
			temp = {typeNames[setType]: list(settingItems.keys())[setChoice-2]}
			return temp

def exportSetMenu():
	exportData = {}
	while (True):
		flagCat = True
		while (flagCat):
			setChoice = setCategoryMenu("(export, enter 0 when ready to export) ")
			if (setChoice == 1):
				return 1
			elif (setChoice == 0):
				flagCat = False
			elif (setChoice == 2):
				setChoice = ui.menu('''\nDo you want to Export ALL settings?
						\n0: Back
						\n1: Exit
						\n2: Yes
						\n3: No
						\n''')
				if (setChoice == 1):
					return 1
				elif (setChoice == 2):
					loc = ui.getLoc(isJustPath = True)
					if (loc == 1):
						return 1
					elif (loc == 0):
						continue
					else:
						exportData = {}
						for i, type in enumerate(sm.returnInfo(0)):
							exportData[type] = []
							settings = sm.returnSet(i)
							for key in settings.keys():
								exportData[type].append(key)
						sm.exportSet(loc, exportData)
						return 0
			else:
				flagItem = True
				while (flagItem):
					itemChoice = setItemMenu(setChoice-3)
					if (itemChoice == 1):
						return 1
					elif (itemChoice == 0):
						flagItem = False
					else:
						for key, value in itemChoice.items():
							if (key in exportData):
								if (value in exportData[key]):
									print("Already in list")
								else:
									exportData[key].append(value)
							else:
								exportData[key] = [value]

		exportChoice = ui.menu('''\nEnter a number from the export menu
				\n0: Back (to settings menu)
				\n1: Exit
				\n2: continue to export
				\n3: select more settings
				\nSelected Settings: '''+str(exportData)+"\n")
		if (exportChoice == 1):
			return 1
		elif (exportChoice == 0):
			return 0
		elif (exportChoice == 3):
			continue
		elif (exportChoice == 2):
			loc = ui.getLoc(isJustPath = True)
			if (loc == 1):
				return 1
			elif (loc == 0):
				continue
			else:
				sm.exportSet(loc, exportData)
				return 0
		else:
			print("Error unknown menu option:", exportChoice)
			return 0

def settingsMenu():
	while (True):
		choice = ui.menu('''\nEnter a number from the Settings menu
				\n0: Back
				\n1: Exit
				\n2: Display
				\n3: Load Cyphers
				\n4: Edit
				\n5: Export
				\n6: Import
				\n''')
		
		if (choice == 0):
			return 0
		elif (choice == 1):
			return 1

		elif (choice == 2):# display
			setChoice = setCategoryMenu("(display) ")
			if (setChoice == 1):
				return 1
			elif (setChoice == 0):
				continue
			elif (setChoice == 2):
				setList = sm.returnInfo(0)
				for i in range(len(setList)):
					sm.display(i)
			else:
				sm.display(setChoice-3)

		elif (choice == 3):# Load Cyphers
			sm.loadCyphers()

		elif (choice == 4):# edit
			flagCat = True
			while (flagCat):
				setChoice = setCategoryMenu("(edit) ", False)
				if (setChoice == 1):
					return 1
				elif (setChoice == 0):
					flagCat = False
				else:
					flagItem = True
					while (flagItem):
						itemChoice = setItemMenu(setChoice-2, True)
						if (itemChoice == 1):
							return 1
						elif (itemChoice == 0):
							flagItem = False
		
		elif (choice == 5):# Export
			exportChoice = exportSetMenu()
			if (exportChoice == 1):
				return 1

		elif (choice == 6):# Import
			impFile = ui.getLoc()
			if (impFile == 1):
				return 1
			elif (impFile == 0):
				continue
			else:
				sm.importSet(impFile)

def mainMenu():
	while (True):
		choice = ui.menu('''\nEnter a number from the menu
				\n1: Exit
				\n2: Encrypt
				\n3: Decrypt
				\n4: RSA Keys
				\n5: Settings
				\n''')
		
		if (choice == 1):
			return 0
		elif (choice == 2):
			choice = encrypterMenu()
		elif (choice == 3):
			choice = decrypterMenu()
		elif (choice == 4):
			choice = rsaMenu()
		elif (choice == 5):
			choice = settingsMenu()
		
		if (choice == 1):
			return 0

mainMenu()
