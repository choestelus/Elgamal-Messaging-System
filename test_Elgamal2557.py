import unittest
from Elgamal2557 import *
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

    def test_string_encrypt(self):
        key = gen_key(1024)
        self.assertEqual(decrypt_string(encrypt_string("hello, world.", key[0]), key), "hello, world.")

    def test_signature(self):
        key = gen_key(5)
        self.assertTrue(verify(3,elgamal_sign(3,key),key[0]))

if __name__ == '__main__':
    unittest.main()

