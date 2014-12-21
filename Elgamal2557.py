import unittest
import os
import binascii
import random
import math
from bitstring import BitArray, BitStream

def isSet(total_num):
    return len(total_num) == len(set(total_num))

def isGenerator(generator_num, mod_num):
    modulus_list = []
    for i in range(1, mod_num):
        t = pow(generator_num, i, mod_num)
        modulus_list.append(t)
    return isSet(modulus_list)

def generatorList(num):
    generator_list = []
    for i in range(1,num - 1):
        if isGenerator(i, num) == True:
            generator_list.append(i)
    return generator_list

def egcd(n1, n2):
    a1, b1, a2, b2 = 1,0,0,1
    while True:
        r, q = n1%n2 , n1//n2
        if(r==0):
            break
        tmp_a2, tmp_b2 = a1-a2*q, b1-b2*q
        n1,n2, a1,b1, a2,b2 = n2,r, a2,b2, tmp_a2,tmp_b2
    gcd = n2
    return gcd, a2, b2

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def exp_mod(x,n,m):
    if n == 0:
        return 1
    elif n == 1:
        return x % m
    elif n%2 == 0:
        return (exp_mod(x,n/2,m)**2) % m
    elif n%2 != 0:
        return (x * exp_mod(x, (n-1)/2 ,m)**2) % m

def getRandomBits(n):
    #n = int(binascii.hexlify(os.urandom(n)), 16)
    return random.SystemRandom().getrandbits(n)

def getRandRange(a, b):
    return random.SystemRandom().randint(a, b)

def lehmannTest(test_number, test_count):
    """docstring for lehmannTest"""
    for i in range(test_count):
        a = getRandRange(1, test_number - 1)
        x = pow(a, (test_number - 1)//2, test_number)
        if not (x == 1 or x == test_number - 1):
            return False
    else:
        return True

def random_generator(p):
    while True:
        g = random.SystemRandom().randint(1,p-1)
        if g != 1%p and g != (-1)%p:
            if exp_mod(g, (p-1)/2, p) != 1:
                return g

def gen_key(p):
    g = random_generator(p)
    u = random.SystemRandom().randint(1, p-1)
    y = exp_mod(g,u,p) #private key
    return [(p,g,y),u]

def encrypt(plaintext, pub_key):
    print pub_key
    p = pub_key[0]
    g = pub_key[1]
    y = pub_key[2]
    block_size = math.floor(math.log(23,2))
    bstream = BitStream()
    for c in plaintext:
        bstream.append("0x" + c.encode("hex"))
    while True:
        k = random.SystemRandom().randint(1, p-1)
        if egcd(k,p-1)[0] == 1:
            break
    #have to add padding to plaintext
    ciphertext = []
    while(bstream.pos < bstream.len):
        x = bstream.read(4).uint
        a = exp_mod(g, k, p)
        b = (exp_mod(y,k, p)*x) % p
        ciphertext.append((a,b))

    print ciphertext
    return ciphertext

def decrypt(ciphertext, key):
    bstream = BitStream()
    plaintext = ""
    for block in ciphertext:
        p, g, y = key[0]
        u = key[1]
        a_pow_u = exp_mod(block[0], u, p)
        inv_a_pow_u = modinv(a_pow_u, p)
        x = (block[1] * inv_a_pow_u) % p
        bstream.append('0x' + str(hex(x)))

    while(bstream.pos < bstream.len):
        plaintext += chr(bstream.read(8).uint)

    return plaintext

def byte_to_binary(n):
    return ''.join(str((n & (1 << i)) and 1) for i in reversed(range(8)))

def hex_to_binary(h):
    return ''.join(byte_to_binary(ord(b)) for b in binascii.unhexlify(h))

def AHash(k,p,bstream):
    block = []
    block_size = (k-1)*math.floor(math.log(p,2))
    if bstream.len % block_size != 0:
        for x in range(0, bstream.len - block_size):
            bstream += 0
    for i in range(0, bstream.len/block_size):
        block[i] = bstream[block_size*i : block_size]

    