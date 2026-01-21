"""
WSL management for KLA Dock
"""

import subprocess
from python.config import WSL_DISTRO
from python import state


def keep_wsl_alive():
    """Keep WSL running in the background"""
    try:
        # Start a persistent process in WSL
        state.wsl_process = subprocess.Popen(
            f'wsl -d {WSL_DISTRO} -- bash -c "while true; do sleep 3600; done"',
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"WSL keepalive process started (PID: {state.wsl_process.pid})")
    except Exception as e:
        print(f"Failed to start WSL keepalive: {e}")


def stop_wsl_keepalive():
    """Stop the WSL keepalive process"""
    if state.wsl_process:
        try:
            state.wsl_process.terminate()
            state.wsl_process.wait(timeout=5)
        except:
            state.wsl_process.kill()
