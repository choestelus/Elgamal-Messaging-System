import unittest
import sys
import os
import binascii
import random
import math
from bitstring import BitArray, BitStream, Bits

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

def bits_of_n(n):
    bits = []
    while n:
        bits.append(n % 2)
        n /= 2

    return bits

def mod_exp(x,n,m):
    result=1
    for bit in reversed(bits_of_n(n)):
        result = result * result % m
        if bit == 1:
            result = result * x % m
    return result

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
    if p == 3:
        return 2

    while True:
        g = random.SystemRandom().randint(1,p-1)
        if g != 1%p and g != (-1)%p:
            if mod_exp(g, (p-1)/2, p) != 1:
                return g

def gen_key(bit_length):
    while(True):
        p = random.SystemRandom().randint(2**(bit_length-1), (2**bit_length)-1)
        if(lehmannTest(p,256)):
            break
    g = random_generator(p)
    u = random.SystemRandom().randint(2**(bit_length-1), p-1)
    y = mod_exp(g,u,p) #private key
    return [(p,g,y),u]

def encrypt(bstream, pub_key):
    p = pub_key[0]
    g = pub_key[1]
    y = pub_key[2]
    ciphertext = [0]

    block_size = int(math.floor(math.log(p,2)))
    ciphertext[0] = bstream.len
    #if bstream.len % block_size != 0:
    #    padding_size = block_size - bstream.len%block_size
    #    bstream.append('0b' + '0'*(padding_size))
    #reset bitstream position
    bstream.pos = 0
    while True:
        k = random.SystemRandom().randint(1, p-1)
        if egcd(k,p-1)[0] == 1:
            break
    #have to add padding to plaintext

    #trying to improve execution speed
    #a = mod_exp(g, k, p)
    while(bstream.pos < bstream.len):
        try:
            #sys.stdout.write(".")
            x = bstream.read(block_size).uint
        except:
            padding_size = block_size - bstream.len%block_size
            x = BitStream("0b" + bstream.read(bstream.len - bstream.pos).bin + "0" * padding_size).uint

        #trying to improve execution speed
        a = mod_exp(g, k, p)
        b = (mod_exp(y,k, p)*x) % p
        ciphertext.append((a,b))

    return ciphertext

def decrypt(ciphertext, key):
    bstream = BitStream()

    p, g, y = key[0]
    u = key[1]

    #trying to improve execution speed
    #a_pow_u = mod_exp(ciphertext[1][0], u, p)
    #inv_a_pow_u = modinv(a_pow_u, p)
    for block in ciphertext[1:]:
        #sys.stdout.write(".")
        #trying to improve execution speed
        a_pow_u = mod_exp(block[0], u, p)
        inv_a_pow_u = modinv(a_pow_u, p)
        x = (block[1] * inv_a_pow_u) % p
        block_size = math.floor(math.log(p,2))
        bstream.append('0b' + bin(x)[2:].zfill(int(block_size)))

    return bstream.read(ciphertext[0])

def encrypt_string(plaintext, pub_key):
    bstream = BitStream()
    for c in plaintext:
        bstream.append("0x" + c.encode("hex"))
    return encrypt(bstream, pub_key)

def decrypt_string(ciphertext, key):
    cipher_bit_stream = decrypt(ciphertext, key)
    plaintext = ""
    while(cipher_bit_stream.pos < cipher_bit_stream.len):
        plaintext += chr(cipher_bit_stream.read(8).uint)
    return plaintext

def elgamal_sign(message, key):
    p = key[0][0]
    g = key[0][1]
    y = key[0][2]
    x = key[1]

    while(True):
        k = random.SystemRandom().randint(1,p-1)
        if egcd(k,p-1)[0] == 1:
            break

    r = mod_exp(g,k,p)
    s = (modinv(k,p-1) * (message-x*r)) % (p-1)

    return (r,s)

def AHash(k,p,bstream):
    block_size = int((k-1)*math.floor(math.log(p,2)))
    n_block = int(math.ceil(bstream.len/float(block_size)))
    message_size = block_size * n_block
    b0 = message_size

    #reset bitstream position
    bstream.pos = 0
    for i in range(1,n_block+1):
        try:
            b0 = roundHash(k, p, BitStream(bstream.read(block_size)), b0)
        except:
            padding_size = block_size - bstream.len%block_size
            b0 = roundHash(k, p,
                BitStream("0b" + bstream.read(bstream.len - bstream.pos).bin + "0" * padding_size),
                b0)

        if(i != n_block):
            tmp_b0 = BitArray("uint:" + str(int(math.ceil(math.log(p,2)))) + "=" + str(b0))
            tmp_b0.ror(int(math.ceil(math.log(p,2))//2))
            b0 = tmp_b0.uint

    return b0

def roundHash(k,p,bstream,b0):
    block_size = int(math.floor(math.log(p,2)))
    result = b0
    while(bstream.pos < bstream.len):
        result = (result + bstream.read(block_size).uint) % p

    return result

def hash_string(k, p, plaintext):
    bstream = BitStream()
    for c in plaintext:
        bstream.append("0x" + c.encode("hex"))
    return AHash(k, p, bstream)

def verify(message,signature,pub_key):
    p = pub_key[0]
    g = pub_key[1]
    y = pub_key[2]

    r = signature[0]
    s = signature[1]
    return mod_exp(g,message,p) == mod_exp(y,r,p)*mod_exp(r,s,p) % p

if __name__ == '__main__':
    key = gen_key(256)
    """message = BitStream(filename="requirements.md")
    ciphertext = encrypt(message, key[0])
    decrypt_text = decrypt(ciphertext, key)"""
