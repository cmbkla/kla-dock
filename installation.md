# KLA Dock - Installation Guide

This guide is for **end users** who want to install and use KLA Dock to manage Docker containers.

> **Are you a developer working on KLA Dock itself?** See the [Development Guide](DEVELOPMENT.md) instead.

---

## 📋 Prerequisites

Before installing KLA Dock, ensure you have:

1. **Windows 10 or 11** with WSL 2 installed
2. **Docker** running in your WSL distribution (Ubuntu recommended)
3. **Docker CLI** installed on Windows
4. Docker CLI configured to connect to your WSL Docker daemon

### Verify Your Setup

Open a Windows command prompt or Git Bash and run:

```bash
docker ps
```

If this shows your containers (or says "no containers"), you're ready to install KLA Dock.

If you get an error, you need to set up Docker in WSL and configure the Windows Docker CLI first.

---

## 🚀 Installation

### Step 1: Download the Installer

Download `KLA_Dock_Setup.exe` from your internal distribution location.

### Step 2: Run the Installer

1. Double-click `KLA_Dock_Setup.exe`
2. Click through the installation wizard
3. **Recommended**: Check "Launch KLA Dock" at the end of installation

### Step 3: Configure Startup (Optional)

The installer gives you the option to run KLA Dock on Windows startup. If you didn't check this during installation, you can set it up later:

**Option A: Using the Installer**
- Re-run the installer and select "Run on startup"

**Option B: Manual Setup via Task Scheduler**
1. Open Task Scheduler (search in Start Menu)
2. Click "Create Task"
3. **General tab**:
   - Name: `KLA Dock`
   - Check "Run whether user is logged on or not"
4. **Triggers tab**:
   - New → "At log on" → Your username
5. **Actions tab**:
   - New → Start a program
   - Program: `C:\Program Files\KLA\KLA Dock\KLA Dock.exe`
6. **Conditions tab**:
   - Uncheck "Start only if on AC power"
7. Click OK

---

## 💡 Using KLA Dock

### System Tray Icon

Once KLA Dock is running, you'll see a hexagonal icon in your system tray (bottom-right of your screen, near the clock).

**Hover over the icon** to see:
- Number of running containers
- Total number of containers

**Right-click the icon** for options:
- **Manage** - Opens the web interface (default action)
- **About** - Shows version and info
- **Quit** - Stops KLA Dock

### Web Interface

Click **Manage** from the system tray menu (or double-click the icon) to open the web dashboard at:

```
http://127.0.0.1:54729
```

#### Containers Section

View all your Docker containers with:
- **Status badge** - Running (green) or Stopped (gray)
- **Container info** - Name, image, ID, ports, creation time
- **Live stats** - CPU%, memory usage, network I/O (for running containers)
- **Actions**:
  - **Start** - Start a stopped container
  - **Stop** - Stop a running container
  - **Restart** - Restart a container
  - **Remove** - Delete a container (asks for confirmation)

#### Images Section

View all your Docker images with:
- **Image info** - Repository, tag, ID, size, creation time
- **Actions**:
  - **Remove** - Delete an image (asks for confirmation)

#### Auto-Refresh

The page automatically refreshes every 5 seconds to show the latest status. You don't need to manually reload.

### Notifications

KLA Dock sends Windows notifications when:
- The app starts successfully
- Container states change (e.g., a container starts or stops)

You can disable notifications in Windows Settings if preferred.

---

## ⚙️ Configuration

KLA Dock works out of the box with default settings. However, you can customize it by editing the configuration (requires stopping the app first):

1. Navigate to: `C:\Program Files\KLA\KLA Dock\`
2. Edit `kla_dock.exe` is standalone, but if you have the source, you can modify:
   - `WEB_PORT` - Change the web interface port (default: 54729)
   - `WSL_DISTRO` - Change your WSL distribution name (default: "Ubuntu")
   - `POLL_INTERVAL` - Change refresh rate in seconds (default: 5)
   - `NOTIFICATION_ENABLED` - Toggle notifications (default: True)

**Note**: The standalone `.exe` has these settings compiled in. To change them, you'll need to rebuild from source (see [Development Guide](DEVELOPMENT.md)).

---

## 🔍 Troubleshooting

### KLA Dock won't start

1. **Check if Docker is running in WSL**:
   - Open WSL: `wsl -d Ubuntu`
   - Run: `docker ps`
   - If Docker isn't running, start it: `sudo service docker start`

2. **Verify Docker CLI on Windows works**:
   ```bash
   docker ps
   ```
   - If this fails, your Docker CLI isn't configured correctly

3. **Check Windows Event Viewer** for error messages:
   - Open Event Viewer → Windows Logs → Application
   - Look for KLA Dock errors

### Docker commands fail in the web interface

1. **Test Docker CLI manually**:
   ```bash
   docker ps
   docker images
   ```
   - If these fail, the issue is with your Docker setup, not KLA Dock

2. **Restart KLA Dock**:
   - Right-click system tray icon → Quit
   - Start KLA Dock again

### Web interface won't open

1. **Check if port 54729 is already in use**:
   ```bash
   netstat -ano | findstr :54729
   ```
   - If another program is using this port, either:
     - Stop that program, or
     - Change KLA Dock's port (requires rebuild from source)

2. **Try accessing directly**:
   - Open browser manually: `http://127.0.0.1:54729`

### WSL still shuts down when I close my terminal

This means KLA Dock isn't running. Check:
- Is the system tray icon visible?
- Is the process running in Task Manager? (Look for "KLA Dock")

### Notifications not appearing

1. **Check Windows notification settings**:
   - Settings → System → Notifications
   - Ensure notifications are enabled
   - Look for "KLA Dock" in the app list

2. **Notifications are optional** - KLA Dock works fine without them

### Port conflict error

If you get an error about port 54729 being in use:

1. **Find what's using the port**:
   ```bash
   netstat -ano | findstr :54729
   ```

2. **Stop the conflicting process** or change KLA Dock's port (requires source rebuild)

---

## 🗑️ Uninstalling

### Using Windows Settings

1. Open **Settings** → **Apps** → **Installed apps**
2. Search for "KLA Dock"
3. Click **Uninstall**

### Using Control Panel

1. Open **Control Panel** → **Programs and Features**
2. Find "KLA Dock"
3. Click **Uninstall**

The uninstaller will:
- Stop KLA Dock if it's running
- Remove all program files
- Remove startup configurations
- Remove registry entries

---

## 📞 Getting Help

If you encounter issues:

1. Check this troubleshooting section first
2. Verify your Docker + WSL setup is working correctly
3. Check the [Development Guide](DEVELOPMENT.md) for technical details
4. Contact your IT team or the KLA Dock maintainer

---

## 🎯 Tips & Best Practices

- **Let KLA Dock run on startup** - This ensures WSL stays alive and Docker is always accessible
- **Keep the web interface bookmarked** - Quick access to `http://127.0.0.1:54729`
- **Use notifications** - They help you catch when containers stop unexpectedly
- **Don't manually close WSL** - Let KLA Dock manage it
- **Check system tray tooltip** - Quick status without opening the web interface

---

**Ready to get started?** Install KLA Dock and enjoy seamless Docker management on Windows!