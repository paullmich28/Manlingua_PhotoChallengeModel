from fastapi import FastAPI, UploadFile, File
from ultralytics import YOLO
from PIL import Image
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
import uvicorn
import io
import socket

app = FastAPI()
model = YOLO("yolov8n.pt")

chat_model = OllamaLLM(model='manlingua-ai')

hostname = socket.gethostname()
IP = socket.gethostbyname(hostname)

class ChatRequest(BaseModel):
    prompt: str

@app.get('/')
async def endpoint():
    return {"Greetings" : "Welcome to Manlingua API"}

@app.get('/get_objects')
async def getItems():
    objects = model.names
    
    object_names = []
    
    for i in objects:
        object_names.append(objects[i])
         
    # print(object_names)
    
    curated_list = [
        "person", "bicycle", "car", "motorcycle", "bench", "bird", "cat", "dog", "backpack", "umbrella",
        "handbag", "tie", "suitcase", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl",
        "banana", "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
        "chair", "couch", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
        "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
        "scissors", "hair drier", "toothbrush"
    ]

    # Filter original_list to keep only items in curated_list
    filtered_list = [item for item in object_names if item in curated_list]
    
    return {"objects": filtered_list}

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

    predictions = []

    # Loop through the results and append each detection to the predictions list
    for result in results:
        for detection in result.boxes:
            class_id = int(detection.cls)
            object_name = result.names[class_id]  # Get object name from class ID
            predictions.append({
                'class': object_name,  # Add the object name instead of just class ID
                'confidence': float(detection.conf)  # Confidence score
            })

    # Return empty predictions if there are none
    if not predictions:
        print("No predictions made by the model")
        return {"error": "No predictions found"}
    
    print(predictions)

    return {'predictions': predictions}

"""AI Chat Simulation"""
@app.post("/generate_chat")
async def getAi(request: ChatRequest):
    result = chat_model.invoke(request.prompt)
    
    return {'response': result}

if __name__ == '__main__':
    uvicorn.run(app, host=IP, port=8000)