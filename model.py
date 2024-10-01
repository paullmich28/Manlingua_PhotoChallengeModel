from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image
import uvicorn
import io

app = FastAPI()

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

    # YOLO Model Prediction
    model = YOLO("yolov8n.pt")
    results = model.predict(img)

    predictions = []
    for result in results:
        for detection in result.boxes:
            predictions.append({
                'class': int(detection.cls), 
                'confidence': float(detection.conf), 
                'box': detection.xyxy.tolist()
            })

    # Return empty predictions if there are none
    if not predictions:
        print("No predictions made by the model")
        return {"error": "No predictions found"}

    return {'predictions': predictions}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)