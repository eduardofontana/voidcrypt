"""VoidCrypt - Secure File Encryption Utility

Lock. Hide. Erase.

A professional-grade CLI file encryption utility implementing
AES-256-GCM with Argon2id key derivation.
"""

__version__ = "1.0.0"
__author__ = "VoidCrypt"
__license__ = "MIT"

from core.crypto import CryptoEngine, EncryptedData
from core.format import VoidcryptFormat
from core.file_handler import FileHandler