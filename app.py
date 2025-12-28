from flask import Flask, request
import cv2
import pytesseract
import numpy as np

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

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    text = pytesseract.image_to_string(gray, config='--psm 8')
    plate = ''.join(filter(str.isalnum, text))

    if plate in registered_numbers:
        return "REGISTERED"
    else:
        return "FAKE"

app.run(host="0.0.0.0", port=5000)
