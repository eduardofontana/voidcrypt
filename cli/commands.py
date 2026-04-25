"""
VoidCrypt - CLI Commands Module

Implements encrypt, decrypt, and info commands.
"""

import os
import time
from typing import Optional
from dataclasses import dataclass

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.table import Table

from core.crypto import CryptoEngine, EncryptedData, secure_delete
from core.file_handler import FileHandler
from core.format import VoidcryptFormat
from core.utils import (
    validate_file, validate_password, format_size, 
    log_operation, secure_input, confirm_action
)


console = Console()


@dataclass
class EncryptOptions:
    """Options for encryption operation."""
    output: Optional[str] = None
    rename: bool = False
    shred: bool = False
    keep_original: bool = True
    hide_filename: bool = False


@dataclass
class DecryptOptions:
    """Options for decryption operation."""
    output: Optional[str] = None
    shred_encrypted: bool = False


class EncryptCommand:
    """Handles file encryption."""
    
    def __init__(self):
        self.crypto = CryptoEngine()
        self.file_handler = FileHandler()
        self.format = VoidcryptFormat()
    
    def execute(
        self, 
        filepath: str, 
        password: str,
        options: Optional[EncryptOptions] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Execute encryption command.
        
        Args:
            filepath: File to encrypt
            password: Encryption password
            options: Encryption options
            
        Returns:
            Tuple of (success, output_file or error_message)
        """
        options = options or EncryptOptions()
        
        is_valid, error = validate_file(filepath)
        if not is_valid:
            return False, error
        
        is_valid, error = validate_password(password)
        if not is_valid:
            return False, error
        
        start_time = time.time()
        
        try:
            original_filename = os.path.basename(filepath) if not options.hide_filename else None
            original_size = os.path.getsize(filepath)
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
                TimeRemainingColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Encrypting...", total=100)
                
                def update_progress(current: int, total: int):
                    percent = int((current / total) * 100)
                    progress.update(task, completed=percent)
                
                file_data = self.file_handler.read_file(
                    filepath, 
                    progress_callback=update_progress
                )
                progress.update(task, completed=30)
                
                encrypted = self.crypto.encrypt(file_data, password)
                progress.update(task, completed=60)
                
                metadata = {
                    "original_size": original_size,
                    "original_filename": original_filename,
                    "timestamp": int(time.time())
                }
                
                encoded = self.format.encode(encrypted, metadata, original_filename)
                progress.update(task, completed=80)
                
                output_path = self.file_handler.generate_output_path(
                    filepath, 
                    options.output,
                    ".void"
                )
                
                if options.rename:
                    output_path = self.file_handler.generate_output_path(
                        filepath, 
                        None,
                        ".void"
                    )
                
                self.file_handler.write_file(
                    output_path, 
                    encoded,
                    progress_callback=update_progress
                )
                progress.update(task, completed=100)
            
            if options.shred and options.keep_original:
                secure_delete(filepath)
            
            duration = time.time() - start_time
            log_operation("ENCRYPT", "SUCCESS", f"{filepath} -> {output_path}")
            
            return True, output_path
            
        except Exception as e:
            log_operation("ENCRYPT", "FAILED", str(e))
            return False, f"Encryption failed: {str(e)}"


class DecryptCommand:
    """Handles file decryption."""
    
    def __init__(self):
        self.crypto = CryptoEngine()
        self.file_handler = FileHandler()
        self.format = VoidcryptFormat()
    
    def execute(
        self, 
        filepath: str, 
        password: str,
        options: Optional[DecryptOptions] = None
    ) -> tuple[bool, Optional[str]]:
        """
        Execute decryption command.
        
        Args:
            filepath: Encrypted file to decrypt
            password: Decryption password
            options: Decryption options
            
        Returns:
            Tuple of (success, output_file or error_message)
        """
        options = options or DecryptOptions()
        
        is_valid, error = validate_file(filepath)
        if not is_valid:
            return False, error
        
        if not self.format.is_voidcrypt_file(filepath):
            return False, "Not a valid voidcrypt file"
        
        start_time = time.time()
        
        try:
            with console.status("[bold red]Decrypting..."):
                with open(filepath, 'rb') as f:
                    data = f.read()
                
                header = self.format.decode(data)
                if header is None:
                    return False, "Invalid file format"
                
                encrypted = EncryptedData(
                    nonce=header.nonce,
                    salt=header.salt,
                    tag=header.tag,
                    ciphertext=header.ciphertext
                )
                
                plaintext = self.crypto.decrypt(encrypted, password)
                
                if plaintext is None:
                    log_operation("DECRYPT", "FAILED", "Wrong password or corrupted")
                    return False, "Decryption failed: wrong password or file corrupted"
                
                metadata = self.format.extract_metadata(header)
                original_filename = metadata.get("original_filename")
                
                output_path = options.output or original_filename
                if not output_path:
                    base = os.path.basename(filepath)
                    output_path = os.path.join(
                        os.path.dirname(filepath),
                        f"decrypted_{base.replace('.void', '')}"
                    )
                
                self.file_handler.write_file(output_path, plaintext)
            
            duration = time.time() - start_time
            log_operation("DECRYPT", "SUCCESS", f"{filepath} -> {output_path}")
            
            return True, output_path
            
        except Exception as e:
            log_operation("DECRYPT", "FAILED", str(e))
            return False, f"Decryption failed: {str(e)}"


class InfoCommand:
    """Handles file info display."""
    
    def __init__(self):
        self.format = VoidcryptFormat()
        self.file_handler = FileHandler()
    
    def execute(self, filepath: str) -> tuple[bool, Optional[dict]]:
        """
        Execute info command.
        
        Args:
            filepath: File to inspect
            
        Returns:
            Tuple of (success, info_dict or error_message)
        """
        is_valid, error = validate_file(filepath)
        if not is_valid:
            return False, error
        
        if not self.format.is_voidcrypt_file(filepath):
            return False, "Not a valid voidcrypt file"
        
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            header = self.format.decode(data)
            if header is None:
                return False, "Invalid file format"
            
            metadata = self.format.extract_metadata(header)
            
            info = {
                "file_size": len(data),
                "file_size_formatted": format_size(len(data)),
                "version": header.version,
                "original_filename": metadata.get("original_filename", "Hidden"),
                "original_size": metadata.get("original_size", 0),
                "original_size_formatted": format_size(metadata.get("original_size", 0)),
                "encrypted_size": len(header.ciphertext),
                "encrypted_size_formatted": format_size(len(header.ciphertext)),
            }
            
            return True, info
            
        except Exception as e:
            return False, f"Failed to read file info: {str(e)}"
    
    def display_info(self, filepath: str) -> None:
        """Display file info in a table."""
        success, result = self.execute(filepath)
        
        if not success:
            console.print(f"[bold red]Error:[/bold red] {result}")
            return
        
        info = result
        
        table = Table(title="[bold cyan]Voidcrypt File Info[/bold cyan]", show_header=False)
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")
        
        table.add_row("File", os.path.basename(filepath))
        table.add_row("Size", info["file_size_formatted"])
        table.add_row("Version", str(info["version"]))
        table.add_row("Original Name", info["original_filename"])
        table.add_row("Original Size", info["original_size_formatted"])
        table.add_row("Encrypted Size", info["encrypted_size_formatted"])
        
        console.print(table)