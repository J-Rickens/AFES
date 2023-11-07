
from tools import setManipulator as sm


def returnRec(recIndex="full"):
	genSet = sm.returnSet(0)
	charList = genSet["charList"]

	recs = {0: charList,
		1: charList.replace("\t","").replace("\n",""),
		2: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
		3.3: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:x",
		3.2: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789:",
		3.1: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-",
		3: "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
		4.1: "0123456789-",
		4: "0123456789"}

	if (recIndex == "full"):
		return recs
	else:
		return recs[recIndex]

def checkIfRec(text, recIndex):
	rec = returnRec(recIndex)
	for c in text:
		if c not in rec:
			return False
	return True