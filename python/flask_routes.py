"""
Flask routes for KLA Dock web interface
"""

import threading
from flask import Flask, render_template_string, jsonify, request
from python.templates import HTML_TEMPLATE
from python import state
from python.config import WEB_PORT
from python.utils import run_command
from python.docker_ops import get_docker_containers, update_docker_state
from python.acr_ops import pull_acr_image, get_acr_repository_tags
from python.notifications import send_notification

# Flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/status')
def api_status():
    # Include active pulls in status (thread-safe copy)
    status = dict(state.docker_state)
    status['active_pulls'] = state.get_active_pulls_copy()
    return jsonify(status)


@app.route('/api/<action>', methods=['POST'])
def api_action(action):
    data = request.json
    target = data.get('target')
    item_type = data.get('type')
    
    if not target or not item_type:
        return jsonify({'success': False, 'error': 'Missing parameters'})
    
    if item_type == 'container':
        if action == 'start':
            cmd = f'docker start {target}'
        elif action == 'stop':
            cmd = f'docker stop {target}'
        elif action == 'restart':
            cmd = f'docker restart {target}'
        elif action == 'remove':
            cmd = f'docker rm -f {target}'
        else:
            return jsonify({'success': False, 'error': 'Unknown action'})
    elif item_type == 'image':
        if action == 'remove':
            cmd = f'docker rmi {target}'
        else:
            return jsonify({'success': False, 'error': 'Unknown action'})
    else:
        return jsonify({'success': False, 'error': 'Unknown type'})
    
    output, code = run_command(cmd)
    
    if code == 0:
        # Update state immediately
        update_docker_state()
        return jsonify({'success': True, 'output': output})
    else:
        return jsonify({'success': False, 'error': output})


@app.route('/api/acr/pull', methods=['POST'])
def api_acr_pull():
    data = request.json
    repository = data.get('repository')
    tag = data.get('tag')
    
    if not repository or not tag:
        return jsonify({'success': False, 'error': 'Missing repository or tag'})
    
    print(f"Starting pull of {repository}:{tag} from ACR...")
    
    # Start pull in background thread (fire and forget for large images)
    def do_pull():
        success, error = pull_acr_image(repository, tag)
        if success:
            update_docker_state()
            send_notification('KLA Dock', f'Pulled {repository}:{tag} from registry')
            print(f"Pull completed: {repository}:{tag}")
        else:
            send_notification('KLA Dock', f'Pull failed: {error}')
            print(f"Pull failed: {repository}:{tag} - {error}")
    
    threading.Thread(target=do_pull, daemon=True).start()
    
    # Return immediately
    return jsonify({'success': True, 'message': 'Pull started in background'})


@app.route('/api/acr/tags')
def api_acr_tags():
    repository = request.args.get('repository')
    
    if not repository:
        return jsonify({'success': False, 'error': 'Missing repository parameter'})
    
    print(f"Fetching tags for {repository}...")
    tags, error = get_acr_repository_tags(repository)
    
    if error:
        return jsonify({'success': False, 'error': error})
    
    return jsonify({'success': True, 'tags': tags})


@app.route('/api/container/start', methods=['POST'])
def api_container_start():
    data = request.json
    image = data.get('image')
    tag = data.get('tag')
    name = data.get('name')
    port = data.get('port')
    password = data.get('password')
    
    if not all([image, tag, name, port, password]):
        return jsonify({'success': False, 'error': 'Missing required parameters'})
    
    # Check if container name already exists
    containers = get_docker_containers()
    if any(c['name'] == name for c in containers):
        return jsonify({'success': False, 'error': f'Container "{name}" already exists. Use a different name or remove the existing container.'})
    
    # Check if port is already in use
    for c in containers:
        if c['state'] == 'running' and c['ports'] and str(port) in c['ports']:
            return jsonify({'success': False, 'error': f'Port {port} is already in use by container "{c["name"]}"'})
    
    # Build docker run command
    full_image = f"{image}:{tag}"
    cmd = (
        f'docker run -e "ACCEPT_EULA=Y" '
        f'-e "SA_PASSWORD={password}" '
        f'-p "{port}:1433" '
        f'-d --name "{name}" '
        f'"{full_image}"'
    )
    
    print(f"Starting container: {cmd}")
    output, code = run_command(cmd, timeout=30)
    
    if code == 0:
        # Update state immediately
        update_docker_state()
        send_notification('KLA Dock', f'Container {name} started')
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': output or 'Failed to start container'})


def run_flask():
    """Run the Flask web server"""
    app.run(host='127.0.0.1', port=WEB_PORT, debug=False, use_reloader=False)
