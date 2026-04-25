"""
VoidCrypt - Utility Functions Module

Logging, validation, and helper functions.
"""

import os
import sys
import logging
from typing import Optional
from datetime import datetime


LOG_DIR = os.path.expanduser("~/.voidcrypt")
LOG_FILE = os.path.join(LOG_DIR, "voidcrypt.log")


def setup_logging(verbose: bool = False) -> logging.Logger:
    """
    Configure logging for voidcrypt.
    
    Args:
        verbose: Enable debug logging
        
    Returns:
        Configured logger
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    
    logger = logging.getLogger("voidcrypt")
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    
    if logger.handlers:
        return logger
    
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_format)
    
    if not logger.handlers:
        logger.addHandler(file_handler)
    
    logger.propagate = False
    
    return logger


def log_operation(operation: str, status: str, details: Optional[str] = None) -> None:
    """Log an operation (no sensitive data)."""
    logger = logging.getLogger("voidcrypt")
    msg = f"{operation}: {status}"
    if details:
        msg += f" | {details}"
    logger.info(msg)


def validate_file(filepath: str) -> tuple[bool, Optional[str]]:
    """
    Validate input file exists and is readable.
    
    Args:
        filepath: Path to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not filepath:
        return False, "No file path provided"
    
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"
    
    if not os.path.isfile(filepath):
        return False, f"Not a file: {filepath}"
    
    if not os.access(filepath, os.R_OK):
        return False, f"File not readable: {filepath}"
    
    return True, None


def validate_password(password: str) -> tuple[bool, Optional[str]]:
    """Validate password meets minimum requirements."""
    if not password:
        return False, "Password cannot be empty"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    return True, None


def format_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def get_timestamp() -> str:
    """Get current timestamp for logging."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def confirm_action(prompt: str) -> bool:
    """Ask user for confirmation."""
    response = input(f"{prompt} [y/N]: ").strip().lower()
    return response in ('y', 'yes')


def secure_input(prompt: str, hide_input: bool = True) -> str:
    """Get secure input from user."""
    if hide_input:
        try:
            import getpass
            return getpass.getpass(prompt)
        except Exception:
            pass
    
    return input(prompt)