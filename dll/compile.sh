#!/bin/bash
# dll/compile.sh

echo "🔧 Compilando DLL para Windows..."

# Compilar versão x64
echo "→ Compilando x64..."
x86_64-w64-mingw32-gcc -shared -o shell_reverse_x64.dll shell_reverse.c -lws2_32 -static -s

# Compilar versão x86
echo "→ Compilando x86..."
i686-w64-mingw32-gcc -shared -o shell_reverse_x86.dll shell_reverse.c -lws2_32 -static -s

echo "✅ DLLs compiladas com sucesso!"
ls -lh *.dll