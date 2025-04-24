from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get-image', methods=['POST'])
def get_image():
    data = request.get_json()
    mark_id = data.get("markId")

    if not mark_id:
        return jsonify({"error": "markId is required"}), 400

    url = "https://piclumen.com/api/image/createdImage"
    headers = {
        "Authorization": "7342faed81997f538bdf6547f1640f467e8e56d1",
        "Accept": "application/json",
        "Platform": "Web"
    }
    payload = { "markId": mark_id }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({
            "error": "Failed to fetch image",
            "status_code": response.status_code,
            "response": response.text
        }), 500

@app.route('/')
def hello():
    return "Piclumen Server is running"
