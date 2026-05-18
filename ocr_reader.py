# models/ocr_reader.py

import cv2
import pytesseract
import re
import numpy as np

# Tesseract path (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -------------------------------------------------
# VEHICLE NUMBER PLATE READER
# -------------------------------------------------

def preprocess_plate(plate_img):

    # Resize image
    plate_img = cv2.resize(plate_img, None, fx=2, fy=2)

    # Convert to grayscale
    gray = cv2.cvtColor(plate_img, cv2.COLOR_BGR2GRAY)

    # Noise removal
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Threshold
    _, thresh = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh


def detect_number_plate(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edged = cv2.Canny(gray, 170, 200)

    contours, _ = cv2.findContours(
        edged.copy(),
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:30]

    for contour in contours:

        peri = cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(
            contour,
            0.018 * peri,
            True
        )

        # Rectangle shape
        if len(approx) == 4:

            x, y, w, h = cv2.boundingRect(contour)

            aspect_ratio = w / float(h)

            # Plate size filtering
            if 2 < aspect_ratio < 6:

                plate = image[y:y + h, x:x + w]

                return plate

    return None


def extract_text_from_plate(plate_img):

    processed = preprocess_plate(plate_img)

    custom_config = r'--oem 3 --psm 8'

    text = pytesseract.image_to_string(
        processed,
        config=custom_config
    )

    # Remove special symbols
    text = re.sub(r'[^A-Z0-9]', '', text.upper())

    return text


def validate_indian_number(text):

    patterns = [
        r'[A-Z]{2}[0-9]{1,2}[A-Z]{1,3}[0-9]{4}',
        r'[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}'
    ]

    for pattern in patterns:

        match = re.search(pattern, text)

        if match:
            return match.group()

    return None


def read_number_plate(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return "IMAGE NOT FOUND"

    # Detect plate
    plate = detect_number_plate(image)

    if plate is None:
        return "PLATE NOT DETECTED"

    # OCR
    text = extract_text_from_plate(plate)

    # Validate
    vehicle_number = validate_indian_number(text)

    if vehicle_number:
        return vehicle_number

    return "UNKNOWN VEHICLE NUMBER"
