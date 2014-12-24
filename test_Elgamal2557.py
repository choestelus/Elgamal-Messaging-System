import unittest
import random
from Elgamal2557 import *
class TestMathProperties(unittest.TestCase):
    def setUp(self):
        pass

    def test_isGenerator(self):
        print "test_isGenerator"
        self.assertTrue(isGenerator(2,11))
        self.assertFalse(isGenerator(3,11))

    def test_lehmannTest(self):
        print "test_lehmannTest"
        self.assertTrue(lehmannTest(2, 256))
        self.assertTrue(lehmannTest(3, 256))
        self.assertTrue(lehmannTest(5, 256))
        self.assertTrue(lehmannTest(7, 256))
        self.assertTrue(lehmannTest(11, 256))
        self.assertTrue(lehmannTest(11, 256))
        self.assertTrue(lehmannTest(1299541, 256))

        self.assertFalse(lehmannTest(488881, 256))

    def test_string_encrypt(self):
        print "test_string_encrypt"
        key = gen_key(256)
        self.assertEqual(decrypt_string(encrypt_string("hello, world.", key[0]), key), "hello, world.")

    def test_file_encrypt(self):
        print "test_file_encrypt"
        key = gen_key(256)
        message = BitStream(filename="README.md")
        ciphertext = encrypt(message, key[0])
        #print "message", len(message), message
        #print ciphertext
        decrypt_text = decrypt(ciphertext, key)
        #print "decrypt_text", len(decrypt_text), decrypt_text
        self.assertEqual(decrypt_text, message)

    def test_signature_string(self):
        message = "digital signature testing"
        key = gen_key(256)
        digest = hash_string(200, key[0][0], message)
        signature = elgamal_sign(digest,key)

        self.assertTrue(verify(digest, signature, key[0]))

    def test_sign_encrypt_file(self):
        key = gen_key(256)

        #encrypt and sign
        message = BitStream(filename="README.md")
        ciphertext = encrypt(message, key[0])
        digest = AHash(100, key[0][0], message)
        signature = elgamal_sign(digest, key)

        #decrypt and verfiy
        plaintext = decrypt(ciphertext, key)
        reciever_digest = AHash(100, key[0][0], plaintext)
        self.assertTrue(verify(reciever_digest, signature, key[0]))
        self.assertTrue(message, plaintext)

    def test_hash(self):
        self.assertEqual(AHash(3, 7, BitStream("0b1010101010101010111111")),6)

if __name__ == '__main__':
    unittest.main()

