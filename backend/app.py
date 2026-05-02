from flask import Flask, request, jsonify, render_template
import subprocess

# FIRST define app
app = Flask(__name__)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Scan route
@app.route('/scan', methods=['POST'])
def scan():
    url = request.json.get('url')

    try:
        command = f"wsl nikto -h {url}"
        result = subprocess.getoutput(command)
    except Exception as e:
        result = str(e)

    return jsonify({"nikto_result": result})

# Run app
if __name__ == '__main__':
    app.run(debug=True)