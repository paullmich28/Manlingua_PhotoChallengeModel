from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from collections import Counter
from PIL import Image
import uvicorn
import io

app = FastAPI()
model = YOLO("yolov8n.pt")

@app.get('/')
async def endpoint():
    return {"Greetings" : "Welcome to Manlingua API"}

@app.post('/predict')
async def predict(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))
        print("Image uploaded successfully")
    except Exception as e:
        print(f"Failed to read the image: {e}")
        return {"error": "Failed to process image"}

    # Perform detection on an image
    results = model.predict(img)

    # Initialize a Counter to keep track of detected object counts
    object_counts = Counter()

    predictions = []

    # Loop through the results and append each detection to the predictions list
    for result in results:
        for detection in result.boxes:
            class_id = int(detection.cls)
            object_name = result.names[class_id]  # Get object name from class ID
            predictions.append({
                'class': object_name,  # Add the object name instead of just class ID
                'confidence': float(detection.conf),  # Confidence score
                'box': detection.xyxy.tolist()  # Bounding box coordinates
            })

    # Return empty predictions if there are none
    if not predictions:
        print("No predictions made by the model")
        return {"error": "No predictions found"}

    return {'predictions': predictions}

if __name__ == '__main__':
    uvicorn.run(app, host='10.60.62.153', port=8000)