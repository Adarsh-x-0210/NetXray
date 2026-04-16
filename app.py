from flask import Flask, request, jsonify
from analyzer import analyze_logs
from log_converter import convert_logs_in_memory

app = Flask(__name__)

@app.route('/')
def home():
    return "NetXray running"

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        file = request.files['logfile']
        lines = file.read().decode().splitlines()

        converted_logs = convert_logs_in_memory(lines)
        result = analyze_logs(converted_logs)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500