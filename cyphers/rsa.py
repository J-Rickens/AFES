# RSA
import rsa

# returnInfo is used to display info about the cypher but also has functional use
# functional info: keepSize - does the ctext length always equals the text length (default False)
#		sizeAdj - to what digree do the lengths differ as a multiple (default 1)
#		inputRec - does the cypher require a spicific input like only numbers and text no symbols can be list of options (default [0])
#		outputRec - what type of outputs are posible only numbers or can be anything, list of options equal to input (default [0])
def returnInfo(choice):

	infoLables = ["name", "description", "keepSize", "sizeAdj", "inputRec", "outputRec"]
	
	info = ["RSA",
		'''description''',
		False,
		1,
		[0],
		[-1]]

	return info[choice]

# Used by encrypt and decrypt to convert the mainKey (large postive int) to what is needed for cypher
def setKey(mainkey):
	ckey = mainkey
	return ckey

# encrypt is a public function to edit the text into cypher text
# opo is the output orination as in what type of input/output rec is outputed
def encrypt(text, mainkey, publicKey):
	key = setKey(mainkey)
	
	ctext = []
	d, r = divmod(len(text), 245)
	for i in range(0,d*245,245):
		ctext.append(rsa.encrypt(text[i:i+245].encode(), publicKey))
	ctext.append(rsa.encrypt(text[r*-1:].encode(), publicKey))
	return ctext, -1

# decrypt is the inverse of encrypt and is a public function
def decrypt(ctext, mainkey, privateKey):
	key = setKey(mainkey)

	text = ""
	for c in ctext:
		text += rsa.decrypt(c, privateKey).decode()
	return text, 0