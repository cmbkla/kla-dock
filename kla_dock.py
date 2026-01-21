#!/usr/bin/env python3
"""
KLA Dock - Main Entry Point
A system tray application to keep WSL running and manage Docker containers/images
"""

import sys
import signal
import time
import threading
import os

# Ensure we're using the correct environment when launched from Windows Explorer
# This fixes issues with Azure CLI and Docker CLI not being found
if sys.platform == 'win32':
    # Add common tool paths to PATH if not already present
    common_paths = [
        r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin",
        r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin",
        r"C:\Program Files\Docker\Docker\resources\bin",
        r"C:\ProgramData\DockerDesktop\version-bin",
    ]

    current_path = os.environ.get('PATH', '')
    for tool_path in common_paths:
        if os.path.exists(tool_path) and tool_path not in current_path:
            os.environ['PATH'] = tool_path + os.pathsep + current_path
            current_path = os.environ['PATH']

# Import all modules
from python.config import WEB_PORT
from python.state import load_active_pulls
from python.wsl_manager import keep_wsl_alive, stop_wsl_keepalive
from python.docker_ops import update_docker_state, background_updater
from python.acr_ops import update_acr_state
from python.notifications import send_notification
from python.flask_routes import run_flask
from python.tray_icon import run_tray_icon


def main():
    """Main application entry point"""
    # Clear debug log on startup
    from python.utils import clear_log_on_startup
    clear_log_on_startup()

    # Write diagnostics to a log file for debugging
    log_file = os.path.expanduser('~/.kla-dock-startup.log')

    def log(message):
        """Log to both console and file"""
        print(message)
        try:
            with open(log_file, 'a') as f:
                f.write(f"{message}\n")
        except:
            pass

    log("=" * 60)
    log("Starting KLA Dock...")
    log(f"Python executable: {sys.executable}")
    log(f"Working directory: {os.getcwd()}")
    log(f"PATH: {os.environ.get('PATH', 'NOT SET')[:300]}...")

    # Test if docker command is available
    try:
        import subprocess
        result = subprocess.run('docker --version', shell=True, capture_output=True, text=True, timeout=5)
        log(f"Docker check: {result.stdout.strip() if result.returncode == 0 else 'NOT FOUND'}")
        if result.returncode != 0:
            log(f"Docker error: {result.stderr}")
    except Exception as e:
        log(f"Docker check failed: {e}")

    # Test if az command is available
    try:
        result = subprocess.run('az --version', shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            log(f"Azure CLI check: OK")
        else:
            log(f"Azure CLI check: NOT FOUND")
            log(f"Azure CLI error: {result.stderr}")
    except Exception as e:
        log(f"Azure CLI check failed: {e}")

    # Set up signal handlers for graceful shutdown
    def signal_handler(sig, frame):
        print("\nShutting down KLA Dock...")
        stop_wsl_keepalive()
        print("KLA Dock stopped.")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Start WSL keepalive
    keep_wsl_alive()
    time.sleep(2)  # Give WSL time to start

    # Load any previously tracked pulls
    load_active_pulls()

    # Initial Docker state update
    update_docker_state()

    # Initial ACR state update (blocking - so UI knows auth status immediately)
    print("Checking Azure CLI authentication...")
    update_acr_state()

    # Send startup notification
    send_notification('KLA Dock', 'Started successfully')

    # Start background updater thread
    updater_thread = threading.Thread(target=background_updater, daemon=True)
    updater_thread.start()

    # Start Flask in a background thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    print(f"Web interface available at: http://127.0.0.1:{WEB_PORT}")

    # Run the system tray icon (this blocks until quit)
    run_tray_icon()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nKLA Dock stopped.")
        sys.exit(0)