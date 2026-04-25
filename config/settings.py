"""
VoidCrypt - Configuration Settings

Default configuration values.
"""

from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class CryptoSettings:
    """Cryptographic configuration."""
    iterations: int = 600000
    nonce_size: int = 12
    salt_size: int = 32
    key_size: int = 32


@dataclass
class FileSettings:
    """File handling configuration."""
    chunk_size: int = 65536
    default_extension: str = ".void"
    compression_enabled: bool = False
    max_file_size: Optional[int] = None


@dataclass
class SecuritySettings:
    """Security configuration."""
    max_attempts: int = 3
    shred_passes: int = 3
    verbose_logging: bool = False
    require_strong_password: bool = True
    min_password_length: int = 8


@dataclass
class Settings:
    """Main configuration container."""
    crypto: CryptoSettings = CryptoSettings()
    file: FileSettings = FileSettings()
    security: SecuritySettings = SecuritySettings()
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Settings":
        """Load settings from file or use defaults."""
        return cls()
    
    def save(self, config_path: Optional[str] = None) -> None:
        """Save settings to file."""
        pass


DEFAULT_SETTINGS = Settings()


def get_settings() -> Settings:
    """Get the default settings."""
    return DEFAULT_SETTINGS