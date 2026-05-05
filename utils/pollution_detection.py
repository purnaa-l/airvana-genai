# utils/pollution_detection.py
import cv2
import numpy as np
from PIL import Image
import tempfile

def analyze(uploaded_file):
    # Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    img = cv2.imread(tmp_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Simple Color Pollution (heaviness based on darkness)
    color_pollution = np.mean(255 - img_rgb)

    # Edge Detection
    edges = cv2.Canny(img, 100, 200)
    edge_pollution = np.sum(edges > 0) / edges.size * 100

    # Simple Waste Detection (count large contours)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    waste_detected = len([c for c in contours if cv2.contourArea(c) > 500])

    # Severity Calculation
    score = (color_pollution * 0.4 + edge_pollution * 0.3 + waste_detected * 10)
    if score < 50:
        severity = "Low"
    elif score < 100:
        severity = "Moderate"
    elif score < 200:
        severity = "High"
    else:
        severity = "Hazardous"

    return color_pollution, edge_pollution, waste_detected, severity
