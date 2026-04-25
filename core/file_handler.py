"""
VoidCrypt - File Handler Module

Handles fileI/O operations with progress tracking and secure memory handling.
"""

import os
from typing import Optional, Callable
from dataclasses import dataclass

CHUNK_SIZE = 64 * 1024


@dataclass
class FileMetadata:
    """Metadata stored in encrypted files."""
    original_filename: Optional[str] = None
    original_size: int = 0
    compressed: bool = False


class FileHandler:
    """Handles file operations with chunked reading for large files."""
    
    @staticmethod
    def read_file(filepath: str, progress_callback: Optional[Callable[[int, int], None]] = None) -> bytes:
        """
        Read file contents with optional progress callback.
        
        Args:
            filepath: Path to file
            progress_callback: Optional callback(processed, total)
            
        Returns:
            File contents as bytes
        """
        file_size = os.path.getsize(filepath)
        
        if file_size < CHUNK_SIZE * 4:
            with open(filepath, 'rb') as f:
                return f.read()
        
        data = bytearray()
        processed = 0
        
        with open(filepath, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                data.extend(chunk)
                processed += len(chunk)
                
                if progress_callback:
                    progress_callback(processed, file_size)
        
        return bytes(data)
    
    @staticmethod
    def write_file(filepath: str, data: bytes, progress_callback: Optional[Callable[[int, int], None]] = None) -> bool:
        """
        Write data to file with optional progress callback.
        
        Args:
            filepath: Output file path
            data: Data to write
            progress_callback: Optional callback(processed, total)
            
        Returns:
            True if successful
        """
        total_size = len(data)
        
        if total_size < CHUNK_SIZE * 4:
            with open(filepath, 'wb') as f:
                f.write(data)
            return True
        
        written = 0
        
        with open(filepath, 'wb') as f:
            while written < total_size:
                chunk = data[written:written + CHUNK_SIZE]
                f.write(chunk)
                written += len(chunk)
                
                if progress_callback:
                    progress_callback(written, total_size)
        
        return True
    
    @staticmethod
    def get_file_info(filepath: str) -> dict:
        """Get basic file information."""
        if not os.path.exists(filepath):
            return {"exists": False}
        
        stat = os.stat(filepath)
        return {
            "exists": True,
            "size": stat.st_size,
            "name": os.path.basename(filepath),
            "path": os.path.abspath(filepath)
        }
    
    @staticmethod
    def generate_output_path(input_path: str, output_file: Optional[str], extension: str = ".void") -> str:
        """Generate output file path."""
        if output_file:
            return output_file
        
        basename = os.path.basename(input_path)
        name_without_ext = os.path.splitext(basename)[0]
        return os.path.join(
            os.path.dirname(input_path),
            f"{name_without_ext}{extension}"
        )