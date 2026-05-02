from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template('index.html')


# ---------------- NIKTO SCAN ----------------
@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"nikto_result": "❌ No URL provided"})

    print(f"[+] Nikto scanning: {url}")

    try:
        process = subprocess.Popen(
            ["nikto", "-h", url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        try:
            # Wait only 15 seconds max
            stdout, stderr = process.communicate(timeout=15)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            return jsonify({
                "nikto_result": "⚠️ Partial scan (stopped after 15 seconds)\n\n" + stdout
            })

        output = stdout if stdout else stderr

        return jsonify({"nikto_result": output})

    except Exception as e:
        return jsonify({"nikto_result": f"❌ Error: {str(e)}"})
# ---------------- NMAP SCAN ----------------
@app.route('/nmap_scan', methods=['POST'])
def nmap_scan():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"result": "❌ No URL provided"})

    print(f"[+] Nmap scanning: {url}")

    try:
        result = subprocess.run(
            ["nmap", "-F", url],
            capture_output=True,
            text=True,
            timeout=30
        )

        output = result.stdout if result.stdout else result.stderr

        return jsonify({"result": output})

    except subprocess.TimeoutExpired:
        return jsonify({"result": "⚠️ Nmap scan timed out"})

    except Exception as e:
        return jsonify({"result": f"❌ Error: {str(e)}"})


# ---------------- RUN SERVER ----------------
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
