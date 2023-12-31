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


@app.route("/printImage/<id>", methods=["GET"])
def printImageAPI(id):
    data = selectImage(id)

    if data == None:
        return "Not Found", 404

    return render_template("image.html", image=imageToBase64(printImage(data[2])))


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

    image2 = imageToBase64(printImage(image))
    image = imageToBase64(centerCrop(image))

    insertImage(id, time, image)

    return jsonify({"id": id, "time": time, "image": image, "printImage": image2})


@app.route("/admin")
def admin():
    pw = request.cookies.get("pw")
    if pw == os.getenv("PW"):
        cur = getImageAll()
        data = cur.fetchone()

        if data is None:
            return "No Image", 404

        renderData = ""

        while data is not None:
            renderData += f'<th><a href="{renderURL}/{data[0]}"><img src="data:image/jpg;base64,{data[2]}" alt="{data[1]}"/></a></th>'

            data = cur.fetchone()

        return render_template("admin.html", data=renderData)
    else:
        res = make_response()
        res.set_cookie("pw", "")
        return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
