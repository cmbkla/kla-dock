# KLA Dock

<p align="center">
  <strong>Docker container management made simple for Windows + WSL</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-success" alt="Status">
  <img src="https://img.shields.io/badge/platform-Windows%20%2B%20WSL-blue" alt="Platform">
  <img src="https://img.shields.io/badge/python-3.8+-blue" alt="Python">
</p>

---

**Built for Kunz, Leigh & Associates**

KLA Dock is a Windows system tray application that keeps WSL running in the background and provides a sleek web interface to manage Docker containers and images. No more manual terminal windows or WSL shutting down unexpectedly.

## ✨ Key Features

### 🔄 **WSL Keepalive**
Automatically keeps your WSL instance running in the background without needing an open terminal window.

### 🎛️ **System Tray Integration**
- Quick access from Windows system tray
- Live status showing running containers
- One-click access to management interface

<img width="274" height="179" alt="image" src="https://github.com/user-attachments/assets/5b1641ef-65ce-4824-8cec-b3b437d38792" />

### 🌐 **Modern Web Interface**
Clean, dark-themed dashboard at `http://127.0.0.1:54729` featuring:
- Real-time container statistics (CPU, memory, network I/O)
- One-click container actions (start, stop, restart, remove)
- Image management and cleanup
- Auto-refreshing every 5 seconds
- Responsive, developer-friendly design

<img width="1141" height="1210" alt="image" src="https://github.com/user-attachments/assets/4068c069-e725-458d-a824-b499c673ef9f" />

### 🔔 **Smart Notifications**
Get notified when container states change with native Windows notifications.

### 🎨 **Developer-Focused Design**
- Geometric, cyberpunk-inspired UI with cyan/green accents
- Dark theme optimized for long coding sessions
- Smooth animations and visual feedback
- JetBrains Mono monospaced fonts

## 📸 What You'll See

The web interface displays:
- **Containers**: All containers with status badges, real-time stats, and quick actions
- **Images**: All Docker images with size info and removal options
- **Live Stats**: CPU percentage, memory usage, and network I/O for running containers
- **Action Feedback**: Visual confirmation of all operations

## 🚀 Getting Started

### For End Users

👉 **[Installation Guide](installation.md)** - Download and install KLA Dock

The installation process is simple:
1. Download the installer
2. Run it
3. KLA Dock starts automatically

### For Developers

👉 **[Development Guide](development.md)** - Set up your dev environment and build from source

Work on KLA Dock itself:
- Set up Python environment
- Build the executable
- Create installers
- Understand the architecture

## 📋 System Requirements

- **Windows 10/11** with WSL 2
- **Docker** running in WSL
- **Docker CLI** installed on Windows (configured to connect to WSL dockerd)

## 🔧 How It Works

1. **WSL Keepalive**: Runs a background process in WSL to prevent auto-shutdown
2. **Flask Web Server**: Serves the management interface on localhost
3. **Docker CLI Integration**: Uses your existing Windows Docker CLI to control containers
4. **System Tray**: Provides quick access and status updates
5. **Polling**: Updates container stats every 5 seconds

## 🛡️ Security

- Web interface is bound to `127.0.0.1` (localhost only)
- Not accessible from the network
- Uses your existing Docker CLI authentication
- No additional credentials needed

## 📚 Documentation

- **[Installation Guide](installation.md)** - For end users installing and using KLA Dock
- **[Development Guide](development.md)** - For developers working on KLA Dock

## 🎯 Why KLA Dock?

If you're running Docker in WSL on Windows, you've probably experienced:
- ❌ WSL shutting down when you close your terminal
- ❌ Having to keep a terminal window open just to keep WSL alive
- ❌ Having to remember CLI commands to see status or do basic tasks

**KLA Dock solves all of this:**
- ✅ WSL stays running automatically in the background
- ✅ Clean, fast web interface
- ✅ Lightweight system tray app
- ✅ Native Windows notifications

## 🏢 About

Developed internally at **Kunz, Leigh & Associates** for our development team's workflow.

## 📝 License

Internal tool for KLA use.

---

<p align="center">
  <strong>Need help?</strong> Check the <a href="installation.md">Installation Guide</a> or <a href="development.md">Development Guide</a>
</p>
