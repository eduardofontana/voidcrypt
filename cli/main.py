"""
VoidCrypt - Main CLI Entry Point

Hacker-style CLI interface with rich output.
"""

import os
import sys
import argparse
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from cli.commands import EncryptCommand, DecryptCommand, InfoCommand, EncryptOptions
from core.utils import secure_input, setup_logging, log_operation


console = Console()


BANNER = """
[bold cyan]
████████╗███████╗██╗     ███████╗██╗  ██╗
╚══██╔══╝██╔════╝██║     ██╔════╝██║  ██║
   ██║   █████╗  ██║     ███████╗███████║
   ██║   ██╔══╝  ██║     ╚════██║██╔══██║
   ██║   ███████╗███████╗███████║██║  ██║
   ╚═╝   ╚══════╝╚══════╝╚══════╝╚═╝  ╚═╝
[/bold cyan]

[italic red]Lock. Hide. Erase.[/italic red]
"""


def print_banner() -> None:
    """Print the ASCII banner."""
    console.print(Panel(BANNER, border_style="cyan", expand=False))


def get_password(confirm: bool = False) -> str:
    """Get password from user securely."""
    while True:
        password = secure_input("[bold cyan]Enter password:[/bold cyan] ")
        
        if not password:
            console.print("[bold red]Password cannot be empty[/bold red]")
            continue
        
        if confirm:
            confirm_password = secure_input("[bold cyan]Confirm password:[/bold cyan] ")
            if password != confirm_password:
                console.print("[bold red]Passwords do not match[/bold red]")
                continue
        
        return password


def encrypt_action(args) -> int:
    """Handle encrypt command."""
    filepath = args.file
    
    if not os.path.exists(filepath):
        console.print(f"[bold red]Error: File not found: {filepath}[/bold red]")
        return 1
    
    password = get_password(confirm=True)
    
    options = EncryptOptions(
        rename=args.rename,
        shred=args.shred,
        keep_original=not args.delete_original
    )
    
    command = EncryptCommand()
    success, result = command.execute(filepath, password, options)
    
    if success:
        console.print(f"[bold green]✓ Encryption complete:[/bold green] {result}")
        return 0
    else:
        console.print(f"[bold red]✗ Encryption failed:[/bold red] {result}")
        return 1


def decrypt_action(args) -> int:
    """Handle decrypt command."""
    filepath = args.file
    
    if not os.path.exists(filepath):
        console.print(f"[bold red]Error: File not found: {filepath}[/bold red]")
        return 1
    
    password = get_password()
    
    command = DecryptCommand()
    success, result = command.execute(filepath, password)
    
    if success:
        console.print(f"[bold green]✓ Decryption complete:[/bold green] {result}")
        return 0
    else:
        console.print(f"[bold red]✗ Decryption failed:[/bold red] {result}")
        return 1


def info_action(args) -> int:
    """Handle info command."""
    filepath = args.file
    
    command = InfoCommand()
    command.display_info(filepath)
    
    return 0


def main() -> int:
    """Main entry point."""
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description="VoidCrypt - Secure File Encryption Utility",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    encrypt_parser = subparsers.add_parser("encrypt", help="Encrypt a file")
    encrypt_parser.add_argument("file", help="File to encrypt")
    encrypt_parser.add_argument("-o", "--output", help="Output file path")
    encrypt_parser.add_argument("-r", "--rename", action="store_true", help="Generate random filename")
    encrypt_parser.add_argument("-s", "--shred", action="store_true", help="Overwrite original file securely")
    encrypt_parser.add_argument("-d", "--delete-original", action="store_true", help="Delete original after encryption")
    
    decrypt_parser = subparsers.add_parser("decrypt", help="Decrypt a file")
    decrypt_parser.add_argument("file", help="File to decrypt")
    decrypt_parser.add_argument("-o", "--output", help="Output file path")
    
    info_parser = subparsers.add_parser("info", help="Show file info")
    info_parser.add_argument("file", help="File to inspect")
    
    args = parser.parse_args()
    
    if not args.command:
        print_banner()
        console.print(Panel(
            "[bold]Usage:[/bold] voidcrypt <command> <file> [options]\n\n"
            "[bold cyan]Commands:[/bold cyan]\n"
            "  encrypt <file>    Encrypt a file\n"
            "  decrypt <file>  Decrypt a file\n"
            "  info <file>     Show file metadata\n\n"
            "[bold cyan]Options:[/bold cyan]\n"
            "  -o, --output         Output file path\n"
            "  -r, --rename        Random output filename\n"
            "  -s, --shred        Secure delete original\n"
            "  -d, --delete-original  Delete original after encryption",
            title="VoidCrypt Help",
            border_style="cyan"
        ))
        return 0
    
    if args.command == "encrypt":
        return encrypt_action(args)
    elif args.command == "decrypt":
        return decrypt_action(args)
    elif args.command == "info":
        return info_action(args)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())