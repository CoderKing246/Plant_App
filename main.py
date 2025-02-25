from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from PIL import Image
import numpy as np
import tensorflow.lite as tflite
import io
import json
import os
import gdown

# Google Drive File ID
file_id = "1ttaB1Llmvm3naGvoTNLc0_kVBtYX-3Ai"
output_path = "models/plant_models.tflite"
#https://drive.google.com/file/d/1ttaB1Llmvm3naGvoTNLc0_kVBtYX-3Ai/view?usp=sharing
# Check if the model already exists
if not os.path.exists(output_path):
    print("Downloading model from Google Drive...")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output_path, quiet=False)
    print("Download completed!")

else:
    print("Model already exists, skipping download.")
app = FastAPI()
# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Load the trained TFLite model
interpreter = tflite.Interpreter(model_path="models/plant_models.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Load plant information database
with open("models/plant_info.json", "r") as f:
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
