"""
Utility functions for KLA Dock
"""

import subprocess
import re
import os
from datetime import datetime


# Log file location
LOG_FILE = os.path.join(os.path.expanduser('~'), 'kla-dock-debug.log')
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB max log size


def clear_log_on_startup():
    """Clear the log file on application startup"""
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
        # Write startup marker
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            f.write(f"=== KLA Dock started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
    except:
        pass


def rotate_log_if_needed():
    """Rotate log file if it gets too large"""
    try:
        if os.path.exists(LOG_FILE):
            size = os.path.getsize(LOG_FILE)
            if size > MAX_LOG_SIZE:
                # Keep last 1MB, discard the rest
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    f.seek(max(0, size - 1024 * 1024))  # Seek to last 1MB
                    f.readline()  # Skip partial line
                    remaining = f.read()

                with open(LOG_FILE, 'w', encoding='utf-8') as f:
                    f.write(f"=== Log rotated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n")
                    f.write(remaining)
    except:
        pass


def log_message(message, is_error=False):
    """Log messages to debug file"""
    try:
        # Rotate if needed (check every 100 messages to avoid overhead)
        import random
        if random.randint(1, 100) == 1:  # 1% chance per message
            rotate_log_if_needed()

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        prefix = "ERROR" if is_error else "INFO"
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] [{prefix}] {message}\n")
    except:
        pass


def find_executable(name, common_paths):
    """Find an executable by checking common paths first, then using 'where' command"""
    # Check common installation paths first (fastest, no subprocess needed)
    for path in common_paths:
        if os.path.exists(path):
            log_message(f"Found {name} at: {path}")
            return path

    # Try 'where' command on Windows as fallback
    try:
        result = subprocess.run(
            f'where {name}',
            shell=True,
            capture_output=True,
            text=True,
            timeout=5,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        if result.returncode == 0 and result.stdout.strip():
            paths = result.stdout.strip().split('\n')
            found_path = paths[0].strip()
            log_message(f"Found {name} via 'where': {found_path}")
            return found_path
    except Exception as e:
        log_message(f"'where {name}' failed: {e}", is_error=True)

    log_message(f"Could not find {name} - using fallback", is_error=True)
    # Fallback to just the command name
    return name


# Cache CLI paths on first lookup
_DOCKER_CMD = None
_AZURE_CMD = None


def get_docker_command():
    """Get the full path to docker executable (cached)"""
    global _DOCKER_CMD
    if _DOCKER_CMD is None:
        common_paths = [
            r"C:\Program Files\Docker\Docker\resources\bin\docker.exe",
            r"C:\Program Files\Docker\Docker\resources\bin\docker.com",
        ]
        _DOCKER_CMD = find_executable('docker', common_paths)
    return _DOCKER_CMD


def get_azure_cli_command():
    """Get the full path to Azure CLI executable (cached)"""
    global _AZURE_CMD
    if _AZURE_CMD is None:
        common_paths = [
            r"C:\Program Files (x86)\Microsoft SDKs\Azure\CLI2\wbin\az.cmd",
            r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az",
            r"C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin\az.exe",
        ]
        _AZURE_CMD = find_executable('az', common_paths)
    return _AZURE_CMD


# Cache the detected DOCKER_HOST
_DOCKER_HOST = None


def detect_docker_host():
    """Detect the correct DOCKER_HOST for Docker in WSL"""
    global _DOCKER_HOST

    if _DOCKER_HOST is not None:
        return _DOCKER_HOST

    # Check if DOCKER_HOST is already set in environment
    existing_host = os.environ.get('DOCKER_HOST')
    if existing_host:
        log_message(f"Using existing DOCKER_HOST from environment: {existing_host}")
        _DOCKER_HOST = existing_host
        return _DOCKER_HOST

    # Try common Docker host configurations
    common_hosts = [
        'tcp://localhost:2375',  # Most common - Docker Desktop WSL integration
        'tcp://127.0.0.1:2375',
        'tcp://localhost:2376',  # TLS variant
        'unix:///var/run/docker.sock',  # Unix socket (less common on Windows)
        'npipe:////./pipe/docker_engine',  # Windows named pipe
    ]

    log_message("DOCKER_HOST not set, attempting auto-detection...")

    # Try each host configuration with a quick version check
    docker_cmd = get_docker_command()

    for host in common_hosts:
        try:
            test_env = os.environ.copy()
            test_env['DOCKER_HOST'] = host

            result = subprocess.run(
                f'"{docker_cmd}" version --format "{{{{.Server.Version}}}}"',
                shell=True,
                capture_output=True,
                text=True,
                timeout=2,
                env=test_env,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if result.returncode == 0 and result.stdout.strip():
                log_message(f"Docker connection successful with DOCKER_HOST={host}")
                _DOCKER_HOST = host
                return _DOCKER_HOST
        except:
            pass

    # If nothing worked, default to most common
    log_message("Could not detect DOCKER_HOST, defaulting to tcp://localhost:2375", is_error=True)
    _DOCKER_HOST = 'tcp://localhost:2375'
    return _DOCKER_HOST


def run_command(cmd, capture_output=True, timeout=10):
    """Execute a shell command and return the result"""
    try:
        actual_cmd = cmd

        # Get environment with DOCKER_HOST set
        env = os.environ.copy()

        # Set DOCKER_HOST for Docker commands and Azure CLI (since az acr login uses Docker)
        if cmd.startswith('docker ') or cmd.startswith('az '):
            detected_host = detect_docker_host()
            env['DOCKER_HOST'] = detected_host

        # Replace command with full path if needed
        if cmd.startswith('docker '):
            docker_path = get_docker_command()
            if docker_path != 'docker':
                actual_cmd = cmd.replace('docker ', f'"{docker_path}" ', 1)
                log_message(f"Running Docker command: {actual_cmd} (DOCKER_HOST={env.get('DOCKER_HOST')})")
        elif cmd.startswith('az '):
            az_path = get_azure_cli_command()
            if az_path != 'az':
                actual_cmd = cmd.replace('az ', f'"{az_path}" ', 1)
                log_message(f"Running Azure CLI command: {actual_cmd} (DOCKER_HOST={env.get('DOCKER_HOST')})")

        # Execute command
        if capture_output:
            result = subprocess.run(
                actual_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )

            if result.returncode != 0:
                log_message(f"Command failed (code {result.returncode}): {actual_cmd}", is_error=True)
                log_message(f"Error output: {result.stderr}", is_error=True)

            return result.stdout.strip(), result.returncode
        else:
            subprocess.Popen(
                actual_cmd,
                shell=True,
                env=env,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
            )
            return "", 0
    except subprocess.TimeoutExpired:
        error_msg = f"Command timed out after {timeout}s: {cmd}"
        log_message(error_msg, is_error=True)
        return error_msg, 1
    except Exception as e:
        error_msg = f"Command exception: {e} | Command: {cmd}"
        log_message(error_msg, is_error=True)
        return str(e), 1


def parse_docker_pull_progress(line):
    """Parse docker pull output for progress information"""
    # Example lines:
    # 9d6cf8f48379: Pulling fs layer
    # 11912f1cc653: Downloading [==>        ] 123MB/456MB
    # 6af2d564f0da: Verifying Checksum
    # 9d6cf8f48379: Download complete
    # 11912f1cc653: Pull complete
    # Already exists

    progress_info = {}

    # Match layer with any status
    match = re.search(r'^([a-f0-9]+):\s+(.+)$', line)
    if match:
        layer_id = match.group(1)
        status_line = match.group(2)
        progress_info['layer_id'] = layer_id

        # Determine status
        if 'Pulling fs layer' in status_line:
            progress_info['layer_status'] = 'Pulling'
        elif 'Waiting' in status_line:
            progress_info['layer_status'] = 'Waiting'
        elif 'Downloading' in status_line:
            progress_info['layer_status'] = 'Downloading'
        elif 'Extracting' in status_line:
            progress_info['layer_status'] = 'Extracting'
        elif 'Verifying Checksum' in status_line:
            progress_info['layer_status'] = 'Verifying'
        elif 'Download complete' in status_line:
            progress_info['layer_status'] = 'Downloaded'
        elif 'Pull complete' in status_line:
            progress_info['layer_status'] = 'Complete'
        elif 'Already exists' in status_line:
            progress_info['layer_status'] = 'Complete'

        # Extract bytes if present
        bytes_match = re.search(r'(\d+\.?\d*[KMGT]?B)/(\d+\.?\d*[KMGT]?B)', status_line)
        if bytes_match:
            progress_info['downloaded'] = bytes_match.group(1)
            progress_info['total'] = bytes_match.group(2)

    return progress_info if progress_info else None


def convert_size_to_bytes(size_str):
    """Convert size string like '123MB' to bytes"""
    if not size_str:
        return 0

    # Handle formats like "123.45MB" or "1.2GB"
    match = re.match(r'(\d+\.?\d*)([KMGT]?B)', size_str)
    if not match:
        return 0

    value = float(match.group(1))
    unit = match.group(2)

    multipliers = {'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4}
    return int(value * multipliers.get(unit, 1))