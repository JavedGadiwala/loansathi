#!/usr/bin/env python3
"""
Windows Executable Builder Script for LoanSathi Personal
Run this to create a standalone .exe file

Usage: python build_windows_exe.py
"""

import os
import sys
import subprocess
from pathlib import Path

def build_exe():
    """
    Build Windows executable using PyInstaller
    """
    print("\n" + "="*60)
    print("LoanSathi Personal - Windows Executable Builder")
    print("="*60 + "\n")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Build command
    base_dir = Path(__file__).parent
    app_file = base_dir / "src" / "app.py"
    build_dir = base_dir / "build"
    dist_dir = base_dir / "dist"
    
    print(f"Source: {app_file}")
    print(f"Build directory: {build_dir}")
    print(f"Output directory: {dist_dir}")
    print("\nBuilding executable...\n")
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "LoanSathi Personal",
        "--distpath", str(dist_dir),
        "--buildpath", str(build_dir),
        "--specpath", str(build_dir),
        str(app_file)
    ]
    
    try:
        subprocess.check_call(cmd)
        print("\n" + "="*60)
        print("Build successful!")
        print(f"\nExecutable location: {dist_dir / 'LoanSathi Personal.exe'}")
        print("\nTo run the application, double-click the .exe file.")
        print("="*60 + "\n")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        return False

if __name__ == "__main__":
    success = build_exe()
    sys.exit(0 if success else 1)
