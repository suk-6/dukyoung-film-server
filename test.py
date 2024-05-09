import requests
import base64
import json

url = "http://localhost:10000/api/image"
# url = 'https://film.wsuk.dev/api/image'

data = {"images": []}

images = ["1.png", "2.png", "3.png", "4.png"]

for i in range(len(images)):
    images[i] = base64.b64encode(open(f"test/{images[i]}", "rb").read()).decode("utf-8")

data["images"] = images
data["frame"] = 0

req = requests.post(url, json=data)

req = json.loads(req.text)

print(req["id"])

with open(f"test/{req['id']}.png", "wb") as f:
    f.write(base64.b64decode(req["image"]))
