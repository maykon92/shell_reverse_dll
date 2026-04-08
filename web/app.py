from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
SERVER_URL = "http://localhost:8000"

@app.route("/")
def dashboard():
    agents = requests.get(f"{SERVER_URL}/agents").json()
    return render_template("dashboard.html", agents=agents)

@app.route("/execute", methods=["POST"])
def execute_command():
    data = request.json
    response = requests.post(f"{SERVER_URL}/execute", json=data)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)