"""
Global state management for KLA Dock
"""

import json
import os
import threading

# Global state
wsl_process = None

docker_state = {
    'containers': [],
    'images': [],
    'stats': {},
    'last_update': None,
    'container_states': {},  # Track previous states for notifications
    'acr_repositories': [],
    'acr_authenticated': False,
    'acr_error': None
}

active_pulls = {}  # Track active image pulls: { "repo:tag": { status, progress, started, ... } }
active_pulls_lock = threading.Lock()  # Thread safety for active_pulls
pulls_file = os.path.expanduser('~/.kla-dock-pulls.json')


def load_active_pulls():
    """Load active pulls from persistent file"""
    global active_pulls
    try:
        if os.path.exists(pulls_file):
            with open(pulls_file, 'r') as f:
                active_pulls = json.load(f)
                print(f"Loaded {len(active_pulls)} active pulls from file")
    except Exception as e:
        print(f"Failed to load pulls file: {e}")
        active_pulls = {}


def save_active_pulls():
    """Save active pulls to persistent file"""
    try:
        with open(pulls_file, 'w') as f:
            json.dump(active_pulls, f)
    except Exception as e:
        print(f"Failed to save pulls file: {e}")


def update_pull_status(key, status_update):
    """Update status of an active pull (thread-safe)"""
    global active_pulls
    with active_pulls_lock:
        if key in active_pulls:
            active_pulls[key].update(status_update)
        else:
            active_pulls[key] = status_update
        save_active_pulls()


def remove_pull_status(key):
    """Remove a pull from active tracking (thread-safe)"""
    global active_pulls
    with active_pulls_lock:
        if key in active_pulls:
            del active_pulls[key]
            save_active_pulls()


def get_active_pulls_copy():
    """Get a thread-safe copy of active_pulls"""
    with active_pulls_lock:
        return dict(active_pulls)
