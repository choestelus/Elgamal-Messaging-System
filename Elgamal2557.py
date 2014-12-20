import unittest
import os
import binascii
import random

def testgen(total_num):
    return len(total_num) == len(set(total_num))

def isGenerator(generator_num, mod_num):
    modulus_list = []
    for i in range(1, mod_num):
        t = pow(generator_num, i, mod_num)
        modulus_list.append(t)
    return testgen(modulus_list)

def generatorList(num):
    generator_list = []
    for i in range(1,num - 1):
        if isGenerator(i, num) == True:
            generator_list.append(i)
    return generator_list

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

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


class TestMathProperties(unittest.TestCase):
    def setUp(self):
        pass

    def test_isGenerator(self):
        self.assertTrue(isGenerator(2,11))
        self.assertFalse(isGenerator(3,11))

    def test_lehmannTest(self):
        self.assertTrue(lehmannTest(2, 256))
        self.assertTrue(lehmannTest(3, 256))
        self.assertTrue(lehmannTest(5, 256))
        self.assertTrue(lehmannTest(7, 256))
        self.assertTrue(lehmannTest(11, 256))
        self.assertTrue(lehmannTest(11, 256))
        self.assertTrue(lehmannTest(1299541, 256))

        
        self.assertFalse(lehmannTest(488881, 256))


if __name__ == '__main__':
    #print "generator", random.SystemRandom().sample(generatorList(23), 1)[0]
    unittest.main()

