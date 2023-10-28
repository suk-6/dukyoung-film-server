import base64
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from io import BytesIO
import qrcode

class generateImage:
    def __init__(self, id, time, images, frame, renderURL):
        self.id = id
        self.time = time
        self.images = images
        self.renderURL = renderURL
        self.frame = Image.open(f"./frames/frame{frame}.png")

    def make(self):
        for i in range(len(self.images)):
            self.images[i] = Image.open(BytesIO(base64.b64decode(self.images[i])))
            self.images[i] = self.images[i].resize((1100, 700))

        canvas = Image.new("RGB", (1200, 3552))
        canvas.paste(self.frame, (0, 0))

        yOffset = 100
        for img in self.images:
            xOffset = (canvas.width - img.width) // 2
            canvas.paste(img, (xOffset, yOffset))
            yOffset += (img.height + 30)

        qr = self.makeQR()

        xOffset = (canvas.width - qr.width - 50)
        yOffset = (canvas.height - qr.height - 50)
        canvas.paste(qr, (xOffset, yOffset))

        xOffset = 50
        yOffset = (canvas.height - 80)
        pos = (xOffset, yOffset)
        canvas = self.drawText(canvas, pos)

        base64Image = imageToBase64(canvas)

        return base64Image
    
    def makeQR(self):
        url = f"{self.renderURL}/{self.id}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr = qr.make_image(fill_color="black", back_color="white")
        qr = qr.resize((100, 100))

        return qr
    
    def drawText(self, canvas, pos):
        draw = ImageDraw.Draw(canvas)

        font = ImageFont.truetype("font.otf", 30)

        draw.text(pos, self.time, (255, 255, 255), font=font)

        return canvas

def imageToBase64(img):
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    buffered.seek(0)

    return base64.b64encode(buffered.getvalue()).decode()

def base64ToImage(base64Image):
    return Image.open(BytesIO(base64.b64decode(base64Image)))

def printImage(img):
    img = base64ToImage(img)
    canvas = Image.new("RGB", (img.size[0] * 2, img.size[1]))
    canvas.paste(img, (0, 0))
    canvas.paste(img, (img.size[0], 0))

    return canvas

if __name__ == '__main__':
    images = ["1.png", "2.png", "3.png", "4.png"]

    for i in range(len(images)):
        images[i] = base64.b64encode(open(f"test/{images[i]}", "rb").read()).decode("utf-8")

    result = generateImage("test", "testTime", images).make()

    print(result)