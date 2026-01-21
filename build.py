#!/usr/bin/env python3
"""
KLA Dock Build Script
Handles building the executable and installer for KLA Dock
"""

import subprocess
import sys
import os
import platform
from pathlib import Path


def print_header(message):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(message)
    print("=" * 60 + "\n")


def print_error(message):
    """Print an error message"""
    print(f"\nERROR: {message}\n")


def print_success(message):
    """Print a success message"""
    print(f"\n{message}\n")


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", "import PyInstaller"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except:
        return False


def install_pyinstaller():
    """Install PyInstaller"""
    print("PyInstaller not found. Installing...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "pyinstaller"],
            check=True
        )
        print_success("PyInstaller installed successfully")
        return True
    except subprocess.CalledProcessError:
        print_error("Failed to install PyInstaller")
        return False


def build_executable():
    """Build the standalone executable with PyInstaller"""
    print_header("KLA Dock - Building Executable")

    # Check if source file exists
    if not Path("kla_dock.py").exists():
        print_error("kla_dock.py not found in current directory")
        return False

    # Check/install PyInstaller
    if not check_pyinstaller():
        if not install_pyinstaller():
            return False

    print("Building standalone executable...\n")

    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "KLA Dock",
        "--icon=NONE",
        "kla_dock.py"
    ]

    try:
        result = subprocess.run(cmd, check=True)

        print_header("Build Completed Successfully!")
        print(f"Executable location: dist{os.sep}KLA Dock.exe\n")
        print("To add to Windows startup:")
        print("1. Press Win+R, type: shell:startup")
        print("2. Create a shortcut to the .exe file\n")
        print("Or see DEVELOPMENT.md for Task Scheduler setup\n")

        return True

    except subprocess.CalledProcessError:
        print_error("Build failed!")
        return False


def check_inno_setup():
    """Check if Inno Setup is installed (Windows only)"""
    if platform.system() != "Windows":
        return False

    possible_paths = [
        r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
        r"C:\Program Files\Inno Setup 6\ISCC.exe",
        r"C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
        r"C:\Program Files\Inno Setup 5\ISCC.exe",
    ]

    for path in possible_paths:
        if Path(path).exists():
            return path

    return None


def build_installer():
    """Build the Windows installer with Inno Setup"""
    print_header("KLA Dock - Building Installer")

    # Check platform
    if platform.system() != "Windows":
        print_error("Installer build is only supported on Windows")
        print("On other platforms, you can only build the executable.")
        return False

    # Check if executable exists
    exe_path = Path("dist") / "KLA Dock.exe"
    if not exe_path.exists():
        print_error("KLA Dock.exe not found in dist/ folder")
        print("\nPlease build the executable first by running:")
        print(f"  python {sys.argv[0]} exe")
        print("  or")
        print(f"  python {sys.argv[0]}")
        return False

    # Check if Inno Setup is installed
    inno_path = check_inno_setup()
    if not inno_path:
        print_error("Inno Setup not found")
        print("\nPlease install Inno Setup from:")
        print("  https://jrsoftware.org/isinfo.php")
        print("\nLooking for ISCC.exe in:")
        print("  C:\\Program Files (x86)\\Inno Setup 6\\")
        print("  C:\\Program Files\\Inno Setup 6\\")
        return False

    # Check if installer script exists
    if not Path("installer.iss").exists():
        print_error("installer.iss not found in current directory")
        return False

    print(f"Found Inno Setup at: {inno_path}")
    print("Building installer with Inno Setup...\n")

    try:
        subprocess.run([inno_path, "installer.iss"], check=True)

        print_header("Installer Built Successfully!")
        print(f"Installer location: Output{os.sep}KLA_Dock_Setup.exe\n")
        print("You can now distribute this installer to users.\n")

        return True

    except subprocess.CalledProcessError:
        print_error("Installer build failed!")
        return False


def show_usage():
    """Show usage information"""
    print("""
KLA Dock Build Script

Usage:
  python build.py [command]

Commands:
  exe, executable    Build the standalone executable (default)
  installer, setup   Build the Windows installer
  all               Build both executable and installer
  help              Show this help message

Examples:
  python build.py              # Build executable only
  python build.py exe          # Build executable only
  python build.py installer    # Build installer only
  python build.py all          # Build both

Notes:
  - Building the installer requires the executable to be built first
  - Installer build only works on Windows with Inno Setup installed
  - See DEVELOPMENT.md for more details
""")


def main():
    """Main entry point"""
    # Determine command
    command = sys.argv[1] if len(sys.argv) > 1 else "exe"
    command = command.lower()

    # Handle commands
    if command in ["help", "-h", "--help"]:
        show_usage()
        return 0

    elif command in ["exe", "executable"]:
        success = build_executable()
        return 0 if success else 1

    elif command in ["installer", "setup"]:
        success = build_installer()
        return 0 if success else 1

    elif command == "all":
        # Build executable first
        if not build_executable():
            return 1

        # Then build installer (if on Windows)
        if platform.system() == "Windows":
            if not build_installer():
                print("\nNote: Executable was built successfully, but installer failed.")
                return 1
        else:
            print("\nNote: Installer build skipped (only available on Windows)")

        return 0

    else:
        print_error(f"Unknown command: {command}")
        show_usage()
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\nBuild cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)