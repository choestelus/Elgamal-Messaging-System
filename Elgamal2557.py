import unittest

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
        print i, isGenerator(i, num)
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

class TestMathProperties(unittest.TestCase):
    def setUp(self):
        pass

    def test_isGenerator(self):
        self.assertTrue(isGenerator(2,11))
        self.assertFalse(isGenerator(3,11))

if __name__ == '__main__':
    unittest.main()
    print isGenerator(3,11)
    print isGenerator(2,11)

