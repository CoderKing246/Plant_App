from fastapi import FastAPI, File, UploadFile
from PIL import Image
import numpy as np
import tensorflow.lite as tflite
import io
import json

app = FastAPI()

# Load the trained TFLite model
interpreter = tflite.Interpreter(model_path="models/plant_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load plant information database
with open("backend/models/plant_info.json", "r") as f:
    plant_info = json.load(f)

def preprocess_image(image):
    image = image.resize((224, 224))  # Resize to match model input
    image = np.array(image) / 255.0  # Normalize
    image = np.expand_dims(image, axis=0).astype(np.float32)
    return image

@app.post("/predict/")
async def predict_plant(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")

    input_data = preprocess_image(image)
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]

    predicted_label = list(plant_info.keys())[np.argmax(predictions)]
    confidence = float(np.max(predictions))

    details = plant_info.get(predicted_label, {})

    return {
        "plant_species": predicted_label,
        "confidence": confidence,
        "details": details
    }
