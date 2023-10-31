from tools import setManipulator as sm
from tools import tempGenerator as tg
from tools import recTool as rt
import random
import rsa

epath = "./downloads/public_key.pem"
file_object = open(epath, 'rb')
publicKey = rsa.PublicKey.load_pkcs1(file_object.read())
file_object.close()
epath = "./downloads/private_key.pem"
file_object = open(epath, 'rb')
privateKey = rsa.PrivateKey.load_pkcs1(file_object.read())
file_object.close()
from cyphers import rsa as cs


#print(tg.createTempCypher("bifid"))
#from cyphers import tempCypher as cs


print(cs.returnInfo(0))
print(cs.returnInfo(1))
print(cs.returnInfo(2))
print(cs.returnInfo(3))
inrec = cs.returnInfo(4)
outrec = cs.returnInfo(5)
print(inrec)
print(outrec)

rectest = 0

testText = ""
testInRec = rt.returnRec(inrec[rectest])
for i in range(999):
    testText += testInRec[random.randint(0,len(testInRec)-1)]
testKey = random.randint(999999,999999999999999)
print("key: ",testKey,"\n")
print("text: ",testText,"\n")

#testcText, a1 = cs.encrypt(testText, testKey)
testcText, a1 = cs.encrypt(testText, testKey, publicKey)
print("ctext: ",testcText,"\n")

#finaltext, a2 = cs.decrypt(testcText, testKey)
finaltext, a2 = cs.decrypt(testcText, testKey, privateKey)
print("ftext: ",finaltext,"\n")


print(inrec)
print(outrec)
print(a1)
print(a2)

print(len(testText))
print(len(testcText))
print(len(finaltext))

if (testText == finaltext):
    print("true")
else:
    print("false")
if (testText != testcText):
    print("true")
else:
    print("false")

'''print("asdfs:")
print(asdf1,asdf2,asdf3,asdf4,asdf5,asdf6,sep="\n",end="\n\n")
if (asdf1 == asdf3):
    print("true")
else:
    print("false")
if (asdf1 == asdf4):
    print("true")
else:
    print("false")
if (asdf2 == asdf3):
    print("true")
else:
    print("false")
if (asdf2 == asdf4):
    print("true")
else:
    print("false")
'''


input('pause')
print(sm.load())
