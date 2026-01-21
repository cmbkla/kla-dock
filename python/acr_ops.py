"""
Azure Container Registry operations for KLA Dock
"""

import json
import subprocess
from datetime import datetime
from python.config import ACR_REGISTRY
from python.utils import run_command, parse_docker_pull_progress
from python.state import update_pull_status, remove_pull_status
from python.docker_ops import update_docker_state
from python.notifications import send_notification


def check_azure_cli():
    """Check if Azure CLI is installed and authenticated"""
    # Check if az command exists
    check_cmd = 'az --version'
    output, code = run_command(check_cmd)
    
    if code != 0:
        return False, "Azure CLI not found or not in PATH"

    # Check if authenticated
    auth_cmd = 'az account show'
    output, code = run_command(auth_cmd)

    if code != 0:
        return False, "Not authenticated with Azure CLI. Please run: az login"

    return True, None


def get_acr_repositories():
    """Get list of repository names from Azure Container Registry"""
    authenticated, error = check_azure_cli()

    if not authenticated:
        return [], False, error

    # Get repository list only (fast)
    cmd = f'az acr repository list --name {ACR_REGISTRY.split(".")[0]} --output json'
    output, code = run_command(cmd, timeout=15)

    if code != 0 or not output:
        return [], True, "Failed to list repositories"

    try:
        repo_names = json.loads(output)
        return repo_names, True, None
    except json.JSONDecodeError:
        return [], True, "Failed to parse repository list"


def get_acr_repository_tags(repository):
    """Get tags for a specific repository"""
    authenticated, error = check_azure_cli()

    if not authenticated:
        return [], error

    # Get tags for specific repository
    cmd = f'az acr repository show-tags --name {ACR_REGISTRY.split(".")[0]} --repository {repository} --output json'
    output, code = run_command(cmd, timeout=30)

    if code != 0 or not output:
        return [], f"Failed to get tags for {repository}"

    try:
        tags = json.loads(output)
        return tags, None
    except json.JSONDecodeError:
        return [], "Failed to parse tags"


def pull_acr_image(repository, tag):
    """Pull an image from Azure Container Registry with progress tracking"""
    authenticated, error = check_azure_cli()

    if not authenticated:
        return False, error

    # Login to ACR (uses cached credentials from az cli)
    login_cmd = f'az acr login --name {ACR_REGISTRY.split(".")[0]}'
    output, code = run_command(login_cmd, timeout=30)

    if code != 0:
        return False, "Failed to authenticate with ACR"

    # Pull the image with progress tracking
    full_image = f'{ACR_REGISTRY}/{repository}:{tag}'
    pull_key = f'{repository}:{tag}'

    # Initialize pull status
    update_pull_status(pull_key, {
        'status': 'pulling',
        'started': datetime.now().isoformat(),
        'progress': 0,
        'layers_complete': 0,
        'layers_total': 0,
        'downloaded_bytes': 0,
        'total_bytes': 0
    })

    try:
        # Get environment with DOCKER_HOST set
        import os
        from python.utils import detect_docker_host, get_docker_command, log_message

        env = os.environ.copy()
        detected_host = detect_docker_host()
        env['DOCKER_HOST'] = detected_host

        # Use full docker path
        docker_cmd = get_docker_command()
        if docker_cmd != 'docker':
            pull_cmd = f'"{docker_cmd}" pull {full_image}'
        else:
            pull_cmd = f'docker pull {full_image}'

        log_message(f"Starting pull: {pull_cmd} (DOCKER_HOST={detected_host})")

        # Run docker pull and capture output in real-time
        process = subprocess.Popen(
            pull_cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            env=env,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )

        layers_seen = {}  # layer_id -> status

        for line in iter(process.stdout.readline, ''):
            if not line:
                break

            line = line.strip()
            log_message(f"Pull output: {line}")

            # Parse progress from line
            progress_info = parse_docker_pull_progress(line)
            if progress_info:
                layer_id = progress_info.get('layer_id')
                layer_status = progress_info.get('layer_status')

                if layer_id and layer_status:
                    # Track this layer
                    layers_seen[layer_id] = layer_status

                    # Count completed layers
                    completed = sum(1 for status in layers_seen.values() if status == 'Complete')
                    total_layers = len(layers_seen)

                    # Calculate progress percentage
                    if total_layers > 0:
                        progress_pct = (completed / total_layers) * 100
                    else:
                        progress_pct = 0

                    # Update pull status
                    update_pull_status(pull_key, {
                        'progress': progress_pct,
                        'layers_complete': completed,
                        'layers_total': total_layers
                    })

        # Wait for process to complete
        process.wait()

        if process.returncode == 0:
            # Pull succeeded - remove from active pulls
            print(f"Pull completed: {pull_key}")
            remove_pull_status(pull_key)
            return True, None
        else:
            # Pull failed
            print(f"Pull failed: {pull_key} - return code {process.returncode}")
            remove_pull_status(pull_key)
            return False, "Pull failed"

    except Exception as e:
        print(f"Pull exception: {pull_key} - {e}")
        remove_pull_status(pull_key)
        return False, str(e)


def update_acr_state():
    """Update ACR repositories list (runs once in background)"""
    from python import state

    # Get ACR repository list (just names, not tags)
    acr_repos = []
    acr_authenticated = False
    acr_error = None
    try:
        print("Fetching ACR repository list...")
        acr_repos, acr_authenticated, acr_error = get_acr_repositories()
        print(f"ACR: Found {len(acr_repos)} repositories, authenticated={acr_authenticated}")
    except Exception as e:
        acr_error = str(e)
        print(f"ACR error: {e}")

    state.docker_state.update({
        'acr_repositories': acr_repos,
        'acr_authenticated': acr_authenticated,
        'acr_error': acr_error
    })