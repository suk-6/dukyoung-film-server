import os
from flask import Flask, request, render_template, jsonify, make_response
from flask_cors import CORS
from db import *
from datetime import datetime
import random
from image import *
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

renderURL = os.getenv("RENDER_URL")


@app.route("/image/<id>", methods=["GET"])
def renderImage(id):
    data = selectImage(id)

    if data == None:
        return "Not Found", 404

    return render_template("image.html", image=data[2])


@app.route("/api/image", methods=["POST"])
def image():
    data = request.get_json()

    now = datetime.now()

    id = f"{datetime.timestamp(now)}.{random.randint(0, 1000000)}"
    time = now.strftime("%Y-%m-%d %H:%M")
    print(id, time)

    frame = data["frame"]
    images = data["images"]
    image = generateImage(id, time, images, frame, renderURL).make()

    insertImage(id, time, image)

    return jsonify({"id": id, "time": time, "image": image})


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        pw = request.body.get("pw")
        if pw == os.getenv("PW"):
            cur = getImageAll()
            data = cur.fetchone()

            if data is None:
                return "No Image", 404

            renderData = f"총 {cur.rowcount}개의 이미지<br>"

            while data is not None:
                renderData += f'<th><a href="{renderURL}/{data[0]}"><img src="data:image/jpg;base64,{data[2]}" alt="{data[1]}"/></a></th>'

                data = cur.fetchone()

            return render_template("admin.html", data=renderData)
    else:
        return """
        <form action="/admin" method="post">
            <input type="password" name="pw">
            <input type="submit">
        </form>
        """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
