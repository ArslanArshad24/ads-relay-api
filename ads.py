from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Relay API running", "routes": ["/relay-get", "/relay-post"]})


@app.route("/relay-get", methods=["POST"])
def relay_get():
    """
    Expects JSON:
    {
        "url": "http://127.0.0.1:50325/api/v1/browser/start",
        "params": {"key": "value"}   # optional
    }
    """
    try:
        data = request.get_json()
        url = data.get("url")
        params = data.get("params", {})

        res = requests.get(url, params=params, timeout=10)

        return jsonify({
            "status": "ok",
            "code": res.status_code,
            "data": res.json() if "application/json" in res.headers.get("content-type", "") else res.text
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/relay-post", methods=["POST"])
def relay_post():
    """
    Expects JSON:
    {
        "url": "http://127.0.0.1:50325/api/v1/browser/start",
        "data": {"key": "value"}   # optional
    }
    """
    try:
        data = request.get_json()
        url = data.get("url")
        payload = data.get("data", {})

        res = requests.post(url, json=payload, timeout=10)

        return jsonify({
            "status": "ok",
            "code": res.status_code,
            "data": res.json() if "application/json" in res.headers.get("content-type", "") else res.text
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
