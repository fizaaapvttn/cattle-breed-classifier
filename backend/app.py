from flask import Flask, request, jsonify
from flask_cors import CORS
from keras.models import load_model
from keras.applications.efficientnet import preprocess_input
from keras.preprocessing import image
import numpy as np
import os
from io import BytesIO

app = Flask(__name__)
CORS(app)  # ✅ Enable CORS for all routes

# Path to your trained model
MODEL_PATH = r"C:\Users\Nishita\Desktop\typ\cattle_fixed.keras"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

model = load_model(MODEL_PATH, custom_objects={"preprocess_input": preprocess_input})

# Example breed labels
class_labels = [
    "amritmahal", "dangi", "gir", "hallikar", "hariana", "jersey cow female diary",
    "kankrej", "khillar", "krishna_valley", "malnad_gidda", "ongole", "rathi",
    "red_sindhi", "sahiwal", "tharparkar", "vechur"
]

@app.route("/")
def home():
    return "Backend is running!"

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    try:
        # Convert FileStorage to BytesIO for load_img
        img = image.load_img(BytesIO(file.read()), target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        # Predict
        preds = model.predict(x)
        pred_index = int(np.argmax(preds))
        confidence = float(np.max(preds) * 100)

        return jsonify({
            "breed": class_labels[pred_index],
            "confidence": round(confidence, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
