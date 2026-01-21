"""
Docker operations for KLA Dock
"""

import json
import time
import threading
from datetime import datetime
from python.utils import run_command
from python import state
from python.config import POLL_INTERVAL
from python.notifications import check_container_changes, NOTIFICATION_ENABLED


def get_docker_containers():
    """Get list of all Docker containers"""
    cmd = 'docker ps -a --format "{{json .}}"'
    output, code = run_command(cmd)
    
    if code != 0 or not output:
        return []
    
    containers = []
    for line in output.split('\n'):
        if line.strip():
            try:
                c = json.loads(line)
                containers.append({
                    'id': c.get('ID', ''),
                    'name': c.get('Names', ''),
                    'image': c.get('Image', ''),
                    'state': c.get('State', ''),
                    'status': c.get('Status', ''),
                    'ports': c.get('Ports', ''),
                    'created': int(c.get('CreatedAt', '0')) if c.get('CreatedAt', '0').isdigit() else 0
                })
            except json.JSONDecodeError:
                continue
    
    return containers


def get_docker_images():
    """Get list of all Docker images"""
    cmd = 'docker images --format "{{json .}}"'
    output, code = run_command(cmd)
    
    if code != 0 or not output:
        return []
    
    images = []
    for line in output.split('\n'):
        if line.strip():
            try:
                img = json.loads(line)
                # Parse size (remove units for now, we'll format in frontend)
                size_str = img.get('Size', '0B')
                size_bytes = 0
                if 'GB' in size_str:
                    size_bytes = float(size_str.replace('GB', '')) * 1024 * 1024 * 1024
                elif 'MB' in size_str:
                    size_bytes = float(size_str.replace('MB', '')) * 1024 * 1024
                elif 'KB' in size_str:
                    size_bytes = float(size_str.replace('KB', '')) * 1024
                
                images.append({
                    'id': img.get('ID', ''),
                    'repository': img.get('Repository', ''),
                    'tag': img.get('Tag', ''),
                    'size': int(size_bytes),
                    'created': 0  # Docker doesn't provide timestamp in this format
                })
            except (json.JSONDecodeError, ValueError):
                continue
    
    return images


def get_container_stats():
    """Get real-time stats for running containers"""
    cmd = 'docker stats --no-stream --format "{{json .}}"'
    output, code = run_command(cmd)
    
    if code != 0 or not output:
        return {}
    
    stats = {}
    for line in output.split('\n'):
        if line.strip():
            try:
                stat = json.loads(line)
                container_id = stat.get('ID', '')
                if container_id:
                    stats[container_id] = {
                        'cpu': stat.get('CPUPerc', 'N/A'),
                        'memory': stat.get('MemPerc', 'N/A'),
                        'net_io': stat.get('NetIO', 'N/A'),
                        'block_io': stat.get('BlockIO', 'N/A')
                    }
            except json.JSONDecodeError:
                continue
    
    return stats


def update_docker_state():
    """Update the global Docker state"""
    containers = get_docker_containers()
    images = get_docker_images()
    stats = get_container_stats()
    
    # Check for container state changes
    if NOTIFICATION_ENABLED:
        check_container_changes(containers)
    
    state.docker_state.update({
        'containers': containers,
        'images': images,
        'stats': stats,
        'last_update': datetime.now().isoformat()
    })


def background_updater():
    """Background thread to update Docker state periodically"""
    while True:
        try:
            update_docker_state()
        except Exception as e:
            print(f"Error updating Docker state: {e}")
        time.sleep(POLL_INTERVAL)
