# KLA Dock - Development Guide

This guide is for **developers** who want to work on KLA Dock itself - modify the code, build from source, or create installers.

> **Just want to use KLA Dock?** See the [Installation Guide](INSTALLATION.md) instead.

---

## 📋 Development Prerequisites

To develop KLA Dock, you need:

1. **Windows 10/11** with WSL 2
2. **Python 3.8 or higher** installed on Windows
3. **Docker** running in WSL
4. **Docker CLI** on Windows (configured to connect to WSL)
5. **Inno Setup** (for building installers) - [Download here](https://jrsoftware.org/isinfo.php)
6. **Git** (optional, for version control)

### Verify Python Installation

```bash
python --version
# Should show Python 3.8 or higher

pip --version
# Should show pip version
```

---

## 🚀 Getting Started

### 1. Clone or Download the Source

Get the KLA Dock source code:

```bash
git clone <repository-url>
cd kla-dock
```

Or download and extract the source ZIP file.

### 2. Install Python Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

This installs:
- **Flask** - Web server
- **Pillow** - Image processing (for system tray icon)
- **pystray** - System tray integration
- **win10toast** - Windows notifications
- **pyinstaller** - Building standalone executables

### 3. Run from Source

Run KLA Dock directly from Python:

```bash
python kla_dock.py
```

You should see:
- Console output: "Starting KLA Dock..."
- System tray icon appears
- Web interface available at http://127.0.0.1:54729
- Windows notification: "KLA Dock started successfully"

**To stop**: Right-click system tray icon → Quit, or press `Ctrl+C` in the console.

---

## 🔧 Project Structure

```
kla-dock/
├── kla_dock.py             # Main application (all-in-one file)
├── requirements.txt        # Python dependencies
├── build.py                # Centralized build script (cross-platform)
├── build.bat               # Windows wrapper for build.py
├── build.sh                # Mac/Linux wrapper for build.py
├── build_all.bat           # Windows wrapper for build.py all
├── build_all.sh            # Mac/Linux wrapper for build.py all
├── build_installer.bat     # Windows installer build wrapper
├── build_installer.sh      # Mac/Linux installer build wrapper
├── installer.iss           # Inno Setup installer script (Windows)
├── README.md               # Project overview
├── INSTALLATION.md         # End user installation guide
└── DEVELOPMENT.md          # This file
```

### Key Files

**kla_dock.py** - The entire application in one file:
- Flask web server with embedded HTML/CSS/JS
- System tray integration
- Docker CLI wrapper functions
- WSL keepalive logic (Windows only)
- Notification system

**requirements.txt** - Python package dependencies

**build.py** - Centralized build script:
- Cross-platform Python build logic
- Handles both executable and installer builds
- Automatic dependency checking
- Clear error messages

**build.bat / build.sh** - Platform-specific wrappers that call build.py

**installer.iss** - Inno Setup script for creating Windows installer

---

## 🏗️ Building KLA Dock

KLA Dock uses a centralized Python build script (`build.py`) that works on all platforms. Convenience wrapper scripts are provided for easy access.

### Building the Standalone Executable

**Windows:**
```bash
build.bat
# or
python build.py
```

**Mac/Linux:**
```bash
./build.sh
# or
python3 build.py
```

This runs PyInstaller with the following options:
- `--onefile` - Single .exe file
- `--windowed` - No console window
- `--name "KLA Dock"` - Application name

The executable will be created in `dist/KLA Dock.exe`

### Building the Windows Installer

**Prerequisites**: Install [Inno Setup](https://jrsoftware.org/isinfo.php) first (Windows only)

**Windows:**
```bash
build_installer.bat
# or
python build.py installer
```

The installer will be created in `Output/KLA_Dock_Setup.exe`

**Note**: Installer build is only available on Windows. On Mac/Linux, you can only build the executable.

### Build All (Executable + Installer)

**Windows:**
```bash
build_all.bat
# or
python build.py all
```

**Mac/Linux:**
```bash
./build_all.sh
# or
python3 build.py all
```

This builds the executable first, then the installer (Windows only).

### Build Script Commands

The `build.py` script supports several commands:

```bash
python build.py              # Build executable only (default)
python build.py exe          # Build executable only
python build.py installer    # Build installer only
python build.py all          # Build both
python build.py help         # Show help
```

The script automatically:
- Checks for and installs PyInstaller if needed
- Verifies files exist before building
- Checks for Inno Setup installation (Windows)
- Provides clear error messages and next steps

---

## ⚙️ Configuration

### Modifying Settings

Edit `kla_dock.py` at the top of the file:

```python
# Configuration
WEB_PORT = 54729              # Port for web interface
WSL_DISTRO = "Ubuntu"         # WSL distribution name
POLL_INTERVAL = 5             # Seconds between stats updates
NOTIFICATION_ENABLED = True   # Enable/disable notifications
```

### Port Number

Default is `54729` - a high, unlikely-to-conflict port. Change if needed:

```python
WEB_PORT = 55000  # or any other port
```

### WSL Distribution

If using a different WSL distro (e.g., Debian):

```python
WSL_DISTRO = "Debian"
```

### Polling Interval

How often to refresh container stats (in seconds):

```python
POLL_INTERVAL = 3  # Faster updates
POLL_INTERVAL = 10 # Slower, less resource usage
```

---

## 🎨 Customizing the UI

The web interface is embedded as an HTML template string in `kla_dock.py`.

### Finding the HTML Template

Search for `HTML_TEMPLATE = '''` in `kla_dock.py`

The template includes:
- HTML structure
- Embedded CSS (in `<style>` tags)
- Embedded JavaScript (in `<script>` tags)

### Modifying Styles

Colors and theme are defined in CSS variables:

```css
:root {
    --bg-primary: #0a0e14;
    --bg-secondary: #151a23;
    --bg-card: #1a1f2e;
    --accent-cyan: #00d4ff;
    --accent-green: #00ff88;
    --accent-orange: #ff6b35;
    --accent-red: #ff3864;
    --text-primary: #e6edf3;
    --text-secondary: #8b949e;
    --border: #30363d;
}
```

### Adding Features

To add new API endpoints:

1. Add a Flask route in `kla_dock.py`:
```python
@app.route('/api/my-feature', methods=['POST'])
def api_my_feature():
    # Your logic here
    return jsonify({'success': True})
```

2. Add JavaScript to call it:
```javascript
async function myFeature() {
    const response = await fetch('/api/my-feature', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
    });
    const result = await response.json();
}
```

3. Add UI elements to trigger it

---

## 🧪 Testing

### Running Tests Manually

1. **Test WSL keepalive**:
   - Start KLA Dock
   - Close any open WSL terminals
   - Wait 1 minute
   - Check if `docker ps` still works from Windows

2. **Test container actions**:
   - Start a container from the web UI
   - Check it started: `docker ps`
   - Stop it from the web UI
   - Check it stopped: `docker ps -a`

3. **Test notifications**:
   - Start/stop a container
   - Verify Windows notification appears

4. **Test system tray**:
   - Check tooltip updates with container count
   - Test all menu items (Manage, About, Quit)

### Common Issues During Development

**Port already in use:**
- Change `WEB_PORT` in the config
- Or kill the process using the port

**Docker commands fail:**
- Verify `docker ps` works from Windows CMD
- Check DOCKER_HOST environment variable

**System tray icon doesn't appear:**
- Check Windows system tray settings
- Look for hidden icons (click ^ in system tray)

---

## 📦 Building for Distribution

### Complete Build Process

1. **Update version number** (in code, installer.iss)

2. **Test thoroughly** from source:
   ```bash
   python kla_dock.py
   ```

3. **Build everything**:
   ```bash
   # Windows
   build_all.bat
   
   # Mac/Linux
   ./build_all.sh
   
   # Or manually
   python build.py all
   ```

4. **Test the builds**:
   ```bash
   # Windows
   dist\"KLA Dock.exe"
   
   # Mac/Linux  
   dist/KLA\ Dock
   ```

5. **Test the installer** (Windows only):
   - Install on a clean machine
   - Verify startup integration
   - Test all features
   - Uninstall cleanly

6. **Distribute**:
   - **Windows**: Share `Output/KLA_Dock_Setup.exe` (installer) or `dist/KLA Dock.exe` (portable)
   - **Mac/Linux**: Share `dist/KLA Dock` (portable executable)

---

## 🏛️ Architecture

### Application Flow

```
main()
  ├─> keep_wsl_alive()          # Background WSL process
  ├─> update_docker_state()      # Initial Docker scan
  ├─> background_updater()       # Thread: polls Docker every 5s
  ├─> run_flask()                # Thread: web server
  └─> pystray.Icon.run()         # Main thread: system tray (blocking)
```

### Threading Model

- **Main thread**: System tray (pystray)
- **Background thread**: Docker state updater
- **Background thread**: Flask web server
- **Background thread**: Tooltip updater
- **Subprocess**: WSL keepalive (`while true; do sleep 3600; done`)

### Docker Integration

All Docker commands use Windows CLI via subprocess:
- `docker ps -a --format "{{json .}}"` - List containers
- `docker images --format "{{json .}}"` - List images
- `docker stats --no-stream --format "{{json .}}"` - Get stats
- `docker start/stop/restart/rm` - Container actions
- `docker rmi` - Remove images

### Web API

Flask endpoints:
- `GET /` - Serve HTML interface
- `GET /api/status` - Get current Docker state (JSON)
- `POST /api/start` - Start container
- `POST /api/stop` - Stop container
- `POST /api/restart` - Restart container
- `POST /api/remove` - Remove container/image

---

## 🔄 Updating Dependencies

To update Python packages:

```bash
pip install --upgrade flask pillow pystray win10toast pyinstaller
pip freeze > requirements.txt
```

Test thoroughly after updates!

---

## 🐛 Debugging

### Enable Console Output

When running the built `.exe`, you won't see console output. To debug:

**Option 1**: Run from source with Python
```bash
python kla_dock.py
```

**Option 2**: Build without `--windowed` flag
```bash
pyinstaller --onefile --name "KLA Dock Debug" kla_dock.py
```

This creates an .exe that shows a console window with output.

### Common Debug Points

Add print statements:
```python
print(f"Docker state: {docker_state}")
print(f"Command output: {output}")
print(f"Error: {e}")
```

### Logging

Consider adding logging for production:
```python
import logging
logging.basicConfig(filename='kla_dock.log', level=logging.INFO)
logging.info("Application started")
```

---

## 🤝 Contributing

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable names
- Add comments for complex logic
- Keep functions focused and small

### Making Changes

1. Create a new branch for your feature
2. Make changes
3. Test thoroughly
4. Update documentation
5. Submit for review

### Testing Checklist

Before submitting changes:
- [ ] Runs from source without errors
- [ ] Builds to .exe successfully
- [ ] All Docker operations work
- [ ] System tray functions correctly
- [ ] Web interface displays properly
- [ ] Notifications appear (if enabled)
- [ ] WSL keepalive works
- [ ] Documentation updated

---

## 📚 Additional Resources

### Python Libraries Used

- **Flask**: https://flask.palletsprojects.com/
- **Pillow**: https://pillow.readthedocs.io/
- **pystray**: https://pystray.readthedocs.io/
- **win10toast**: https://github.com/jithurjacob/Windows-10-Toast-Notifications
- **PyInstaller**: https://pyinstaller.org/

### Tools

- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **Python**: https://www.python.org/
- **Docker**: https://www.docker.com/
- **WSL**: https://learn.microsoft.com/en-us/windows/wsl/

---

## 🎯 Future Enhancements

Potential features to add:
- Azure Container Registry integration
- Container logs viewer
- Volume management
- Network management
- Docker Compose support
- Custom container creation UI
- Stats graphs and history
- Export/import container configs
- Multi-WSL distribution support
- Mac support (menu bar app)

---

**Happy coding!** If you have questions, check the [Installation Guide](INSTALLATION.md) or [README](README.md).