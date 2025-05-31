import ast
from flask import Flask, request, jsonify
import os
import subprocess
import re

app = Flask(__name__)

# Secure password handling
PASSWORD = os.getenv("PASSWORD", "defaultpassword")

@app.route('/')
def hello():
    name = request.args.get('name', 'World')
    if not name.isalnum():
        return jsonify({"error": "Invalid name"}), 400
    return f"Hello, {name}!"

@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    # Validate IP format
    if not re.match(r"^\d{1,3}(\.\d{1,3}){3}$", ip):
        return jsonify({"error": "Invalid IP format"}), 400

    try:
        result = subprocess.check_output(
            ["ping", "-c", "1", ip],
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return jsonify({"error": str(e.output)}), 500

@app.route('/calculate')
def calculate():
    expr = request.args.get('expr', '')

    # Secure evaluation: Only allow numeric expressions
    try:
        parsed = ast.parse(expr, mode='eval')
        if not all(isinstance(node, (ast.Expression, ast.BinOp, ast.Num, ast.operator)) for node in ast.walk(parsed)):
            raise ValueError("Unsafe expression")
        result = eval(compile(parsed, '<string>', mode='eval'))
        return str(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

