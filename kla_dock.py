#!/usr/bin/env python3
"""
KLA Dock - Main Entry Point
A system tray application to keep WSL running and manage Docker containers/images
"""

import sys
import signal
import time
import threading

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
    print("Starting KLA Dock...")
    
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
    
    # Initial ACR state update (one time, in background)
    acr_init_thread = threading.Thread(target=update_acr_state, daemon=True)
    acr_init_thread.start()
    
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
