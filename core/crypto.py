"""
VoidCrypt - Core Cryptography Module

Implements military-grade encryption using AES-256-GCM with PBKDF2 key derivation.
"""

import os
import hashlib
from typing import Optional
from dataclasses import dataclass

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend


NONCE_SIZE = 12
SALT_SIZE = 32
KEY_SIZE = 32
TAG_SIZE = 16
ITERATIONS = 600000


@dataclass
class EncryptedData:
    """Container for encrypted data with all cryptographic components."""
    nonce: bytes
    salt: bytes
    tag: bytes
    ciphertext: bytes


class CryptoEngine:
    """
    Core cryptographic engine implementing AES-256-GCM encryption.
    
    Uses PBKDF2 for secure key derivation.
    Each encryption operation generates fresh random values for nonce and salt.
    """
    
    def __init__(self, iterations: int = ITERATIONS):
        """
        Initialize the crypto engine.
        
        Args:
            iterations: Number of PBKDF2 iterations (default 600k)
        """
        self.iterations = iterations
    
    def derive_key(self, password: str, salt: bytes) -> bytes:
        """
        Derive a 256-bit key from password using PBKDF2.
        
        Args:
            password: User password
            salt: Random salt bytes
            
        Returns:
            32-byte derived key
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))
    
    def encrypt(self, plaintext: bytes, password: str) -> EncryptedData:
        """
        Encrypt plaintext using AES-256-GCM.
        
        Generates fresh random nonce and salt for each operation.
        
        Args:
            plaintext: Data to encrypt
            password: Encryption password
            
        Returns:
            EncryptedData containing nonce, salt, tag, and ciphertext
        """
        salt = os.urandom(SALT_SIZE)
        nonce = os.urandom(NONCE_SIZE)
        
        key = self.derive_key(password, salt)
        aesgcm = AESGCM(key)
        
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        
        tag = ciphertext[-TAG_SIZE:]
        ciphertext = ciphertext[:-TAG_SIZE]
        
        return EncryptedData(
            nonce=nonce,
            salt=salt,
            tag=tag,
            ciphertext=ciphertext
        )
    
    def decrypt(self, encrypted: EncryptedData, password: str) -> Optional[bytes]:
        """
        Decrypt data using AES-256-GCM.
        
        Verifies authentication tag before returning plaintext.
        Returns None if decryption fails (wrong password or tampering).
        
        Args:
            encrypted: EncryptedData to decrypt
            password: Decryption password
            
        Returns:
            Decrypted plaintext or None if failed
        """
        try:
            salt = encrypted.salt
            key = self.derive_key(password, salt)
            aesgcm = AESGCM(key)
            
            ciphertext_with_tag = encrypted.ciphertext + encrypted.tag
            plaintext = aesgcm.decrypt(encrypted.nonce, ciphertext_with_tag, None)
            
            return plaintext
        except Exception:
            return None
    
    @staticmethod
    def derive_key_from_password(password: str, salt: bytes) -> bytes:
        """Static method for key derivation without instance configuration."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=KEY_SIZE,
            salt=salt,
            iterations=ITERATIONS,
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))


def generate_random_filename(extension: str = ".void") -> str:
    """Generate a random filename for encrypted files."""
    random_bytes = os.urandom(16)
    return hashlib.sha256(random_bytes).hexdigest()[:32] + extension


def secure_delete(filepath: str, passes: int = 3) -> bool:
    """
    Simulate secure file deletion by overwriting with random data.
    
    Note: This is a simulation. For true secure deletion, use specialized tools.
    
    Args:
        filepath: Path to file to delete
        passes: Number of overwrite passes
        
    Returns:
        True if successful
    """
    try:
        file_size = os.path.getsize(filepath)
        
        with open(filepath, 'r+b') as f:
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(file_size))
                f.flush()
        
        os.remove(filepath)
        return True
    except Exception:
        return False