from flask import Flask, request
import cv2
import pytesseract
import numpy as np
import os

app = Flask(__name__)

registered_numbers = [
    "TN01AB1234",
    "KA05CD6789",
    "MH12EF3456"
]

@app.route('/upload', methods=['POST'])
def upload():
    data = np.frombuffer(request.data, np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)

    if img is None:
        return "FAKE"

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    text = pytesseract.image_to_string(
        gray,
        config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    )

    plate = ''.join(filter(str.isalnum, text))

    if plate in registered_numbers:
        return "REGISTERED"
    else:
        return "FAKE"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
