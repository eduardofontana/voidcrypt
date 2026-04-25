"""
VoidCrypt - File Format Module

Custom binary file format for encrypted files.
Format: [MAGIC][VERSION][SALT][NONCE][TAG][METADATA][CIPHERTEXT]
"""

import struct
import json
from typing import Optional
from dataclasses import dataclass

from core.crypto import EncryptedData, SALT_SIZE, NONCE_SIZE, TAG_SIZE


MAGIC = b'VOID'
VERSION = 1
METADATA_SIZE = 256


@dataclass
class VoidcryptHeader:
    """Header structure for encrypted files."""
    magic: bytes
    version: int
    salt: bytes
    nonce: bytes
    tag: bytes
    metadata: bytes
    ciphertext: bytes
    
    @property
    def total_size(self) -> int:
        """Calculate total file size."""
        return (len(self.magic) + 4 + 
                len(self.salt) + len(self.nonce) + len(self.tag) +
                METADATA_SIZE + len(self.ciphertext))


class VoidcryptFormat:
    """Handles custom binary format encoding/decoding."""
    
    @staticmethod
    def encode(encrypted: EncryptedData, metadata: dict, original_filename: Optional[str] = None) -> bytes:
        """
        Encode encrypted data into custom binary format.
        
        Args:
            encrypted: EncryptedData object
            metadata: Metadata dictionary
            original_filename: Optional original filename to hide
            
        Returns:
            Binary formatted data
        """
        metadata_json = json.dumps(metadata)
        metadata_bytes = metadata_json.encode('utf-8')
        
        metadata_padded = metadata_bytes.ljust(METADATA_SIZE, b'\x00')
        
        result = bytearray()
        result.extend(MAGIC)
        result.extend(struct.pack('!I', VERSION))
        result.extend(encrypted.salt)
        result.extend(encrypted.nonce)
        result.extend(encrypted.tag)
        result.extend(metadata_padded)
        result.extend(encrypted.ciphertext)
        
        return bytes(result)
    
    @staticmethod
    def decode(data: bytes) -> Optional[VoidcryptHeader]:
        """
        Decode binary format back to components.
        
        Args:
            data: Binary data
            
        Returns:
            VoidcryptHeader or None if invalid
        """
        offset = 0
        
        magic = data[offset:offset + 4]
        offset += 4
        
        if magic != MAGIC:
            return None
        
        version_data = data[offset:offset + 4]
        version = struct.unpack('!I', version_data)[0]
        offset += 4
        
        if version != VERSION:
            return None
        
        salt = data[offset:offset + SALT_SIZE]
        offset += SALT_SIZE
        
        nonce = data[offset:offset + NONCE_SIZE]
        offset += NONCE_SIZE
        
        tag = data[offset:offset + TAG_SIZE]
        offset += TAG_SIZE
        
        metadata_bytes = data[offset:offset + METADATA_SIZE]
        offset += METADATA_SIZE
        
        metadata = metadata_bytes.rstrip(b'\x00')
        
        ciphertext = data[offset:]
        
        return VoidcryptHeader(
            magic=magic,
            version=version,
            salt=salt,
            nonce=nonce,
            tag=tag,
            metadata=metadata,
            ciphertext=ciphertext
        )
    
    @staticmethod
    def extract_metadata(header: VoidcryptHeader) -> dict:
        """Extract metadata from header."""
        try:
            metadata_json = header.metadata.decode('utf-8')
            return json.loads(metadata_json)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}
    
    @staticmethod
    def is_voidcrypt_file(filepath: str) -> bool:
        """Check if file is a valid voidcrypt file."""
        try:
            with open(filepath, 'rb') as f:
                magic = f.read(4)
                return magic == MAGIC
        except Exception:
            return False