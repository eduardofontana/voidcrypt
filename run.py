"""
VoidCrypt - Run Entry Point

Main entry point for running voidcrypt.
"""

import sys
import os


def main():
    """Main entry point."""
    from cli.main import main as cli_main
    sys.exit(cli_main())


if __name__ == "__main__":
    main()