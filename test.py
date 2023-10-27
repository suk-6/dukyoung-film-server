import requests
import base64

url = 'http://localhost:10000/api/image'

data = {
    "images": []
}

images = ["1.png", "2.png", "3.png", "4.png"]

for i in range(len(images)):
    images[i] = base64.b64encode(open(f"test/{images[i]}", "rb").read()).decode("utf-8")

data['images'] = images

requests.post(url, json=data)