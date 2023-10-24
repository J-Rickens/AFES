# This is a template for creating/adding new cyphers for AFES
# There are 4 defined functions that must be updated and the names cannot be changed

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
# inputRec and outputRec both are represented by numbers as defined bellow: (more values can be added as needed)
# 0: any and all posible caracters in char list
# 1: any and all posible caracters in char list except \t\n
# 2: a-z, A-Z, 0-9
# 3: A-Z, 0-9	.1: A-Z, 0-9, -	.2: A-Z, 0-9, :	.3: A-Z, 0-9, :, x
# 4: 0-9	.1: 0-9, -
def returnInfo(choice):

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["bifid",
		'''description''',
		False,
		1,
		[0],
		[0]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey):
	ckey = mainkey
	return ckey

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey):
	key = setKey(mainkey)
	ctext = text
	return ctext, opo

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey):
	key = setKey(mainkey)
	text = ctext
	return text, opo