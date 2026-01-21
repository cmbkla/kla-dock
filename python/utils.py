"""
Utility functions for KLA Dock
"""

import subprocess
import re


def run_command(cmd, capture_output=True, timeout=10):
    """Execute a shell command and return the result"""
    try:
        if capture_output:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout.strip(), result.returncode
        else:
            subprocess.Popen(cmd, shell=True)
            return "", 0
    except subprocess.TimeoutExpired:
        print(f"Command timed out after {timeout}s: {cmd}")
        return "", 1
    except Exception as e:
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
