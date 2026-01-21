# KLA Dock - Development Guide

This guide is for **developers** who want to work on KLA Dock itself - modify the code, build from source, or create installers.

> **Just want to use KLA Dock?** See the [Installation Guide](installation.md) instead.

---

## 📋 Development Prerequisites

To develop KLA Dock, you need:

1. **Windows 10/11** with WSL 2
2. **Python 3.8 or higher** installed on Windows
3. **Docker** running in WSL
4. **Docker CLI** on Windows (configured to connect to WSL)
5. **Azure CLI** (for Azure Container Registry features) - [Download here](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
6. **Inno Setup** (for building installers) - [Download here](https://jrsoftware.org/isinfo.php)
7. **Git** (optional, for version control)

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
- **win11toast** - Windows 11 notifications
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
├── kla_dock.py                 # Main application entry point
├── python/                     # Application modules
│   ├── __init__.py            # Package marker
│   ├── config.py              # Configuration constants
│   ├── state.py               # Global state management
│   ├── utils.py               # Shared utilities
│   ├── wsl_manager.py         # WSL keepalive management
│   ├── notifications.py       # Windows notification system
│   ├── docker_ops.py          # Docker operations
│   ├── acr_ops.py             # Azure Container Registry operations
│   ├── templates.py           # HTML/CSS/JS template (embedded)
│   ├── flask_routes.py        # Flask web API routes
│   └── tray_icon.py           # System tray functionality
├── requirements.txt           # Python dependencies
├── build.py                   # Centralized build script (cross-platform)
├── build.bat                  # Windows wrapper for build.py
├── build.sh                   # Mac/Linux wrapper for build.py
├── build_all.bat              # Windows wrapper for build.py all
├── build_all.sh               # Mac/Linux wrapper for build.py all
├── installer.iss              # Inno Setup installer script (Windows)
├── .gitignore                 # Git ignore patterns
├── readme.md                  # Project overview
├── installation.md            # End user installation guide
└── DEVELOPMENT.md             # This file
```

### Module Overview

| Module | Lines | Purpose |
|--------|-------|---------|
| **kla_dock.py** | 73 | Main entry point - orchestrates all modules |
| **config.py** | 17 | Configuration constants (ports, settings) |
| **state.py** | 73 | Thread-safe global state management |
| **utils.py** | 106 | Shared utilities (command execution, parsing) |
| **wsl_manager.py** | 30 | WSL keepalive process management |
| **notifications.py** | 56 | Windows notification system |
| **docker_ops.py** | 146 | Docker container/image operations |
| **acr_ops.py** | 217 | Azure Container Registry operations |
| **templates.py** | 1,752 | Embedded HTML/CSS/JS web interface |
| **flask_routes.py** | 174 | Flask web API endpoints |
| **tray_icon.py** | 107 | System tray icon and menu |

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

This runs PyInstaller which:
- Bundles all Python modules from `python/` directory
- Embeds the HTML/CSS/JS template
- Creates a single `.exe` file (Windows) or executable (Mac/Linux)
- Uses flags: `--onefile`, `--windowed`, `--name "KLA Dock"`

The executable will be created in `dist/KLA Dock.exe`

### Building the Windows Installer

**Prerequisites**: Install [Inno Setup](https://jrsoftware.org/isinfo.php) first (Windows only)

The build script checks for Inno Setup in these locations:
- `C:\Program Files (x86)\Inno Setup 6\`
- `C:\Program Files\Inno Setup 6\`
- `%LOCALAPPDATA%\Programs\Inno Setup 6\` (user install)

**Windows:**
```bash
python build.py installer
```

The installer will be created in `dist/KLA_Dock_Setup.exe`

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
- Verifies source files exist before building
- Checks for Inno Setup installation (Windows)
- Provides clear error messages and next steps

### Build Output

After running `build.py all`, you'll have:

```
dist/
├── KLA Dock.exe          # Standalone executable
└── KLA_Dock_Setup.exe    # Windows installer
```

Both files can be committed to the repository or distributed.

---

## ⚙️ Configuration

### Modifying Settings

Edit `python/config.py`:

```python
# Web server configuration
WEB_PORT = 54729

# WSL configuration
WSL_DISTRO = "Ubuntu"

# Docker polling interval
POLL_INTERVAL = 5  # seconds between Docker stats updates

# Notifications
NOTIFICATION_ENABLED = True

# Azure Container Registry
ACR_REGISTRY = "kunzleigh.azurecr.io"
```

---

## 🎨 Customizing the UI

The web interface is embedded in `python/templates.py`.

### Modifying Styles

Colors and theme are defined in CSS variables at the top of the template:

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

### Module-Specific Changes

- **Docker operations**: Edit `python/docker_ops.py`
- **ACR operations**: Edit `python/acr_ops.py`
- **Notifications**: Edit `python/notifications.py`
- **System tray**: Edit `python/tray_icon.py`
- **Web routes**: Edit `python/flask_routes.py`
- **State management**: Edit `python/state.py`

