"""
VoidCrypt - Tests

Test the encryption/decryption cycle and error handling.
"""

import os
import tempfile
import unittest
from unittest import TestCase

from core.crypto import CryptoEngine, EncryptedData
from core.format import VoidcryptFormat
from core.file_handler import FileHandler


class TestCrypto(TestCase):
    """Test cryptographic operations."""
    
    def setUp(self):
        self.crypto = CryptoEngine()
        self.format = VoidcryptFormat()
        self.file_handler = FileHandler()
        self.test_data = b"This is secret data " * 100
        self.password = "SecurePassword123!"
    
    def test_encrypt_decrypt(self):
        """Test basic encrypt/decrypt cycle."""
        encrypted = self.crypto.encrypt(self.test_data, self.password)
        
        self.assertIsInstance(encrypted, EncryptedData)
        self.assertEqual(len(encrypted.nonce), 12)
        self.assertEqual(len(encrypted.salt), 32)
        self.assertEqual(len(encrypted.tag), 16)
        
        decrypted = self.crypto.decrypt(encrypted, self.password)
        
        self.assertEqual(decrypted, self.test_data)
    
    def test_wrong_password(self):
        """Test decryption with wrong password fails."""
        encrypted = self.crypto.encrypt(self.test_data, self.password)
        
        result = self.crypto.decrypt(encrypted, self.password + "wrong")
        
        self.assertIsNone(result)
    
    def test_file_format(self):
        """Test binary file format encoding/decoding."""
        encrypted = self.crypto.encrypt(self.test_data, self.password)
        
        metadata = {
            "original_size": len(self.test_data),
            "original_filename": "secret.txt"
        }
        
        encoded = self.format.encode(encrypted, metadata, "secret.txt")
        
        self.assertIsInstance(encoded, bytes)
        self.assertTrue(encoded.startswith(b'VOID'))
        
        header = self.format.decode(encoded)
        
        self.assertIsNotNone(header)
        self.assertEqual(header.version, 1)
    
    def test_file_handler(self):
        """Test file read/write operations."""
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(self.test_data)
            tmp_path = tmp.name
        
        try:
            read_data = self.file_handler.read_file(tmp_path)
            self.assertEqual(read_data, self.test_data)
            
            output_path = tmp_path + ".out"
            self.file_handler.write_file(output_path, read_data)
            
            verify_data = self.file_handler.read_file(output_path)
            self.assertEqual(verify_data, self.test_data)
            
            os.remove(output_path)
        finally:
            os.remove(tmp_path)
    
    def test_is_voidcrypt_file(self):
        """Test voidcrypt file detection."""
        encrypted = self.crypto.encrypt(self.test_data, self.password)
        
        metadata = {"original_filename": "test.txt"}
        
        encoded = self.format.encode(encrypted, metadata)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".void") as tmp:
            tmp.write(encoded)
            tmp_path = tmp.name
        
        try:
            is_valid = self.format.is_voidcrypt_file(tmp_path)
            self.assertTrue(is_valid)
        finally:
            os.remove(tmp_path)


if __name__ == "__main__":
    unittest.main()