"""
System tray icon for KLA Dock
"""

import sys
import time
import threading
import webbrowser
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
from python.config import WEB_PORT, POLL_INTERVAL
from python import state
from python.notifications import send_notification
from python.wsl_manager import stop_wsl_keepalive


def create_tray_icon():
    """Create a system tray icon"""
    # Create a simple geometric icon (hexagon for container/docker theme)
    size = 64
    image = Image.new('RGB', (size, size), color=(10, 14, 20))
    draw = ImageDraw.Draw(image)

    # Draw hexagon
    center = size // 2
    radius = size // 2 - 4
    points = []
    for i in range(6):
        angle = i * 60 - 30  # Start from top
        x = center + radius * (1 if i % 3 == 0 else 0.5) * (1 if i < 3 else -1)
        y = center + radius * 0.866 * (1 if 1 <= i <= 4 else -0.5)
        points.append((x, y))

    draw.polygon(points, outline=(0, 212, 255), width=3)
    draw.ellipse([center-3, center-3, center+3, center+3], fill=(0, 255, 136))

    return image


def get_tray_tooltip():
    """Generate tooltip text for system tray"""
    try:
        containers = state.docker_state.get('containers', [])
        running = sum(1 for c in containers if c['state'] == 'running')
        total = len(containers)

        return f"KLA Dock\n{running}/{total} containers running"
    except:
        return "KLA Dock"


def open_web_interface(icon, item):
    """Open the web interface in default browser"""
    webbrowser.open(f'http://127.0.0.1:{WEB_PORT}')


def show_about(icon, item):
    """Show about dialog"""
    send_notification(
        'KLA Dock',
        f'Version 1.0\nManage Docker on WSL\nWeb UI: http://127.0.0.1:{WEB_PORT}'
    )


def quit_application(icon, item):
    """Quit the application"""
    # Stop WSL keepalive process
    stop_wsl_keepalive()
    icon.stop()


def run_tray_icon():
    """Create and run the system tray icon"""
    # Create system tray icon
    icon_image = create_tray_icon()
    menu = pystray.Menu(
        item('Manage', open_web_interface, default=True),
        item('About', show_about),
        pystray.Menu.SEPARATOR,
        item('Quit', quit_application)
    )

    icon = pystray.Icon(
        "kla_dock",
        icon_image,
        "KLA Dock",
        menu
    )

    # Update tooltip periodically
    def update_tooltip():
        while True:
            icon.title = get_tray_tooltip()
            time.sleep(POLL_INTERVAL)

    tooltip_thread = threading.Thread(target=update_tooltip, daemon=True)
    tooltip_thread.start()

    # Run the system tray icon (this blocks)
    try:
        icon.run()
    finally:
        # Clean up when icon stops
        # Only print/flush if stdout exists (not available in windowed .exe)
        if sys.stdout:
            print("\nKLA Dock stopped. Press Enter to continue...")
            sys.stdout.flush()