import os
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from db import insertImage, selectImage
from datetime import datetime
import random
from image import generateImage
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

renderURL = os.getenv("RENDER_URL")

@app.route('/image/<id>', methods=['GET'])
def renderImage(id):
    data = selectImage(id)

    if data == None:
        return "Not Found", 404

    return render_template("image.html", image=data[2])


@app.route('/api/image', methods=['POST'])
def image():
    data = request.get_json()

    now = datetime.now()

    id = f"{datetime.timestamp(now)}.{random.randint(0, 1000000)}"
    time = now.strftime("%Y-%m-%d %H:%M")

    print(id, time)
    image = generateImage(id, time, data['images'], renderURL).make()

    insertImage(id, time, image)

    return jsonify({"image": image})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)