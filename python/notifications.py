"""
Windows notification system for KLA Dock
"""

from python.config import NOTIFICATION_ENABLED
from python import state

# Try to import win11toast for notifications
try:
    from win11toast import toast
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    print("win11toast not available - notifications disabled")


def send_notification(title, message):
    """Send a Windows notification"""
    print(f"Notification: {title} - {message}")  # Debug logging
    if NOTIFICATION_ENABLED and NOTIFICATIONS_AVAILABLE:
        try:
            # Call synchronously - win11toast might not be thread-safe
            toast(title, message)
        except Exception as e:
            print(f"Notification failed: {e}")
    else:
        if not NOTIFICATION_ENABLED:
            print("Notifications disabled")
        if not NOTIFICATIONS_AVAILABLE:
            print("win11toast not available")


def check_container_changes(current_containers):
    """Check for container state changes and send notifications"""
    for container in current_containers:
        container_id = container['id']
        current_state = container['state']
        previous_state = state.docker_state['container_states'].get(container_id)
        
        # Debug logging
        if previous_state != current_state:
            print(f"State change detected: {container['name']} {previous_state} -> {current_state}")
        
        if previous_state and previous_state != current_state:
            send_notification(
                'KLA Dock',
                f"Container {container['name']} {current_state}"
            )
        
        state.docker_state['container_states'][container_id] = current_state
