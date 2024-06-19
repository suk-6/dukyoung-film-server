from PIL import Image
from io import BytesIO
import base64
import sqlite3

conn = sqlite3.connect("images.sqlite", check_same_thread=False)

c = conn.cursor()


def getImageAll():
    return c.execute("SELECT * FROM images ORDER BY time DESC")


def base64ToImage(base64Image):
    return Image.open(BytesIO(base64.b64decode(base64Image)))


def saveImage(base64Image, id):
    base64ToImage(base64Image).save(f"./extract/{id}.png")


if __name__ == "__main__":
    images = getImageAll()
    for image in images:
        saveImage(image[2], image[0])
        print(f"Saved image {image[0]}")
