import random
import os
from tools import setManipulator as sm

# add function to convert to pkcs(8)

# Sorces used to make rabinMiller and genPrimNum functions:
# https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_creating_rsa_keys.htm
# https://www.geeksforgeeks.org/primality-test-set-3-miller-rabin/

def millerRabin(num):
	k = 5

	d = num - 1
	r = 0
	while (d%2 == 0):
		d = d//2
		r += 1

	for i in range(k):
		a = random.randint(2,num-1)
		x = (a**d)%num
		if (x != 1 and x != num-1):
			flag = True
			j = 0
			while (flag):
				j += 1
				x = (x**2)%num
				if (x==1):
					return False
				if (x==num-1):
					flag = False
				if (j >= (r)):
					flag = False

	return True

def genPrimNum(bitSize):
	minSize = 2
	if (bitSize < minSize):
		print("Error with Key Size(min:"+minSize+"):"+bitSize)
		return "error"

	lowPrimes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
		73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163,
		167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257,
		263, 269, 271, 277, 281, 283, 293, 307, 311, 313,317, 331, 337, 347, 349, 353, 359,
		367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461,
		463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577,
		587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677,
		683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809,
		811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919,
		929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

	while(True):
		num = random.randint((2**(bitSize-1)),(2**bitSize))
		if (num in lowPrimes):
			return num
		flag = True
		for prime in lowPrimes:
			if (num % prime == 0):
				flag = False
		if (flag):
			if (millerRabin(num)):
				return num

# Used ChatGPT to make extended_gcd function to find d
# OpenAI. (2023). ChatGPT (September 25 Version) [Large language model]. https://chat.openai.com
def extended_gcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = extended_gcd(b % a, a)
        return (g, y - (b // a) * x, x)

def saveKeys(name,n,e,d):
	pyloc = os.getcwd()
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
	
	print(name)
	print(n)
	print(e)
	print(d)
	print(locPri)
	print(locPub)
	return 1

def genKeys(name):
	settings = sm.returnSet(3)
	if (settings == "error"):
		return settings

	bitSize = 20#settings["size"]
	p = genPrimNum(bitSize)
	q = genPrimNum(bitSize)
	while (p == q):
		q = genPrimNum(bitSize)

	n = p*q
	t = (p-1)*(q-1)
	e = random.randint(2, t)
	g, d, _ = extended_gcd(e, t)
	while (e%p == 0 or e%q == 0 or g > 1):
		e = random.randint(2, t)
		g, d, _ = extended_gcd(e, t)
	if d < 0:
		d += t

	if (saveKeys(name,n,e,d) == "error"):
		return "error"
	return 1