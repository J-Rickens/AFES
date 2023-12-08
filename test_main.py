
import importlib
from tools import encrypter as e
from tools import decrypter as d
def ee(layers = 3, sizeMulti = 0, text = "", locText = "", locSave = "", isPassword = False, isRSA = False, mainkey = "", genkey = 0):
    importlib.reload(e)
    return e.encrypt(layers, sizeMulti, text, locText, locSave, isPassword, isRSA, mainkey, genkey)

def er(layers = 3, sizeMulti = 0, text = "", locText = "", locSave = "", isPassword = False, publicKeyName = ""):
    importlib.reload(e)
    return e.encryptWithRSA(layers, sizeMulti, text, locText, locSave, isPassword, publicKeyName)

def de(ctext, layers = 3, sizeMulti = 0, locSave = "", isPassword = False, mainkey = "", currentOpo = 0):
    importlib.reload(d)
    importlib.reload(e)
    return d.decrypt(ctext, layers, sizeMulti, locSave, isPassword, mainkey, currentOpo)

def dr(ctext, privateKeyName, layers = 3, sizeMulti = 0, locSave = "", isPassword = False):
    importlib.reload(d)
    importlib.reload(e)
    return d.decryptWithRSA(ctext, privateKeyName, layers, sizeMulti, locSave, isPassword)

loc = "C:\\Users\\Stickens\\Desktop\\GIT\\projects\\AFES other\\text.txt"
el = 5
es = 100
print("encrypting...")
ctext, cloc, chash = ee(layers = el,sizeMulti = es,locText = loc)
print(ctext, cloc, chash, "Done\n", sep ="\n")

print("decrypting...")
ttext, tloc, thash = de(ctext,layers = el,sizeMulti = es)
print(ttext, tloc, thash, "Done\n", sep ="\n")

rl = 3
rs = 100
print("encrypting rsa...")
ctext, cloc, chash, keyname = er(layers = rl,sizeMulti = rs,locText = loc, publicKeyName = "")
print(ctext, cloc, chash, keyname, "Done\n", sep ="\n")

print("decrypting rsa...")
ttext, tloc, thash = dr(ctext,keyname,layers = rl,sizeMulti = rs)
print(ttext, tloc, thash, "Done\n", sep ="\n")


"""from tools import setManipulator as sm
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



import codecs
import os
import hashlib
hashlib.algorithms_available
hashSettings['saltEn'] = codecs.encode(os.urandom(hashSettings['sizeEn']),'hex').decode()
hashSettings['saltSt'] = codecs.encode(os.urandom(hashSettings['sizeSt']),'hex').decode()

"""
