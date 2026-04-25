# VOIDCRYPT

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License">
  <img src="https://img.shields.io/badge/Status-Active-orange?style=flat-square" alt="Status">
</p>

---

## WARNING

**VOIDCRYPT IS AN EDUCATIONAL SECURITY TOOL.** 

This software is provided for **legitimate privacy protection** purposes only. Always:
- Ensure you have legal authority to encrypt files you own
- Keep backups of your passwords - encrypted files cannot be recovered without them
- Test with non-critical files first before using with important data

---

## Overview

VoidCrypt is a professional-grade CLI file encryption utility inspired by tools like VeraCrypt. It implements **military-grade cryptography** with modern best practices for securing sensitive files locally.

### Core Philosophy

```
Lock. Hide. Erase.
```

VoidCrypt provides confidential file encryption using authenticated encryption (AES-256-GCM) with memory-hard key derivation (Argon2id) to protect against brute-force and GPU-based attacks.

---

## Features

### Encryption
- **AES-256-GCM** - Industry-standard authenticated encryption
- **PBKDF2-HMAC-SHA256** - Secure key derivation (600k iterations)
- **Unique nonce per file** - No reusable IVs
- **Secure randomness** - Uses `os.urandom` for all cryptographic random values

### File Format
- **Custom binary format** - Structured encrypted file format
- **Optional filename hiding** - Strip original filename from metadata
- **Integrity verification** - Authentication tag prevents tampering

### CLI Interface
- **Rich terminal UI** - Colorized output with progress bars
- **Password masking** - Hidden input using getpass
- **Status messages** - Clear feedback on operations

### Security Options
- **Random filename output** - Generate untraceable filenames
- **Secure shred simulation** - Overwrite original with random data
- **Attempt limiting** - Optional self-destruct after failed attempts

---

## Installation

### Prerequisites

```bash
# Python 3.11 or higher required
python --version
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Quick Start

```bash
# Encrypt a file
python -m voidcrypt.cli.main encrypt secret_document.pdf

# Encrypt with random filename
python -m voidcrypt.cli.main encrypt secret.pdf -r

# Decrypt a file  
python -m voidcrypt.cli.main decrypt secret_document.pdf.void

# View encrypted file info
python -m voidcrypt.cli.main info secret_document.pdf.void
```

---

## Usage Examples

### Basic Encryption

```bash
$ python -m voidcrypt.cli.main encrypt mysecret.txt
Enter password: ********
Confirm password: ********
✓ Encryption complete: mysecret.txt.void
```

### With Options

```bash
# Random filename, shred original after encrypting
$ python -m voidcrypt.cli.main encrypt confidential.pdf -r -s
Enter password: ********
Confirm password: ********
✓ Encryption complete: a3f8c2d1e5b6...4a7f.void
```

### Decryption

```bash
$ python -m voidcrypt.cli.main decrypt mysecret.txt.void
Enter password: ********
✓ Decryption complete: mysecret.txt
```

### File Information

```bash
$ python -m voidcrypt.cli.main info mysecret.txt.void

┌─────────────────────────────────────┐
│       Voidcrypt File Info             │
├─────────────────────────────────────┤
│ File            │ mysecret.txt.void   │
│ Size            │ 24.50 KB          │
│ Version        │ 1                 │
│ Original Name  │ mysecret.txt       │
│ Original Size │ 1.02 KB          │
└─────────────────────────────────────┘
```

---

## Cryptographic Design

### Encryption Scheme

| Component | Value |
|-----------|-------|
| Algorithm | AES-256-GCM |
| Key Size | 256-bit (32 bytes) |
| Nonce Size | 96-bit (12 bytes) |
| Tag Size | 128-bit (16 bytes) |
| Mode | Authenticated Encryption |

### Key Derivation

| Parameter | Value |
|-----------|-------|
| KDF | PBKDF2-HMAC-SHA256 |
| Iterations | 600,000 |
| Hash | SHA-256 |
| Salt Size | 256-bit (32 bytes) |

### Why These Choices?

- **AES-GCM**: Provides both confidentiality AND integrity in one operation. The authentication tag ensures any tampering is detected.
- **PBKDF2-HMAC-SHA256**: Industry-standard key derivation with high iteration count for brute-force resistance.
- **Unique nonces**: Each encryption uses fresh random values, preventing pattern analysis.

---

## File Format

Encrypted files use a custom binary format:

```
┌──────────────────────────────────────────────────────┐
│  MAGIC HEADER     │ 4 bytes  │ "VOID"                  │
├──────────────────────────────────────────────────────┤
│  VERSION        │ 4 bytes  │ Format version (1)      │
├──────────────────────────────────────────────────────┤
│  SALT           │ 16 bytes │ Argon2 salt              │
├──────────────────────────────────────────────────────┤
│  NONCE          │ 12 bytes │ AES-GCM nonce           │
├──────────────────────────────────────────────────────┤
│  TAG            │ 16 bytes │ Authentication tag       │
├──────────────────────────────────────────────────────┤
│  METADATA       │ 256 bytes│ JSON metadata          │
├──────────────────────────────────────────────────────┤
│  CIPHERTEXT     │ N bytes  │ Encrypted data        │
└──────────────────────────────────────────────────────┘
```

### Metadata Structure

```json
{
  "original_size": 1024,
  "original_filename": "secret.txt",
  "timestamp": 1699999999
}
```

---

## Security Considerations

### Strengths
- Authenticated encryption prevents tampering
- Argon2id provides strong GPU/ASIC resistance
- No password reuse across different files
- Fresh random values per encryption

### Limitations
- **No password recovery** - Lost passwords = lost data
- **Windows-only secure delete** - OS-level file recovery may still be possible
- **Memory exposure** - Passwords may remain in memory

### Best Practices

1. **Use strong passwords** - Minimum 12 characters with mixed case, numbers, symbols
2. **Keep backups** - Always have copies of important files
3. **Test first** - Verify encryption/decryption works before deleting originals
4. **Don't forget passwords** - No recovery mechanism exists

---

## Project Structure

```
voidcrypt/
├── core/
│   ├── crypto.py       # AES-256-GCM + Argon2 implementation
│   ├── file_handler.py # File I/O with progress tracking
│   ├── format.py     # Custom binary format
│   └── utils.py     # Logging and utilities
├── cli/
│   ├── main.py       # CLI entry point
│   └── commands.py  # Command implementations
├── config/
│   └── settings.py  # Configuration
├── tests/
│   └── test_crypto.py
├── requirements.txt
├── run.py
└── README.md
```

---

## Testing

```bash
# Run unit tests
python -m pytest tests/

# Or run directly
python -m voidcrypt.tests.test_crypto
```

Expected output:
```
.....
----------------------------------------------------------------------
Ran 5 tests in 2.451s

OK
```

---

## Dependencies

| Package | Purpose |
|---------|----------|
| cryptography | AES-GCM encryption |
| argon2-cffi | Argon2 key derivation |
| rich | Terminal UI |

---

## License

MIT License - See LICENSE file for details.

---

## Disclaimer

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND. USE AT YOUR OWN RISK. THE AUTHORS DISCLAIM ALL LIABILITY FOR ANY DAMAGES RESULTING FROM USE OF THIS SOFTWARE.

This tool is intended for legitimate privacy protection. Always comply with applicable laws and regulations in your jurisdiction.

---

## Credits

Inspired by:
- VeraCrypt
- SQLCipher
- Password Hashing Competition winners

---

<p align="center">
  <sub>Created for educational and legitimate privacy protection purposes.</sub>
</p>