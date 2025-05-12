from flask import Flask, request, jsonify
import requests
import time

app = Flask(__name__)

HEADERS = {
    "Authorization": "7342faed81997f538bdf6547f1640f467e8e56d1",
    "Accept": "application/json",
    "Platform": "Web",
    "Content-Type": "application/json"
}

@app.route('/check_image', methods=['POST'])
def check_image():
    data = request.get_json()
    mark_id = data.get('markId')

    if not mark_id:
        return jsonify({"error": "markId is required"}), 400

    url = "https://piclumen.com/api/image/createdImage"
    payload = {"markId": mark_id}

    # Ждём максимум 60 секунд, проверяя каждые 5
    for _ in range(12):
        res = requests.post(url, json=payload, headers=HEADERS)

        try:
            res_data = res.json()
        except:
            res_data = {}

        # Успешный ответ
        if res.status_code == 200 and res_data.get("status") == 0:
            image_data = res_data.get("data", [])
            if image_data and image_data[0].get("img_urls"):
                return jsonify({
                    "image_url": image_data[0]["img_urls"][0]["imgUrl"]
                })

        # Подождать перед следующей попыткой
        time.sleep(5)

    return jsonify({"error": "Image not ready after timeout"}), 504

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
