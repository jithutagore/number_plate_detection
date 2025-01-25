import cv2
from fastapi import FastAPI, File, UploadFile,HTTPException
from model_loader import NumberPlateDetection
from AI.yolov5.detect import run
import uvicorn
import numpy as np
from processImage import inferenceImage
from traffiicDbOperation import *
from dotenv import load_dotenv
load_dotenv()
api_host=os.getenv("API_HOST")
api_port=os.getenv("API_PORT")


app = FastAPI()

# Initialize the models globally
number_plate_detection = NumberPlateDetection()

# Get YOLO model components
yolo_model, stride, name, pt = number_plate_detection.get_yolo_model()
text_conversion_model = number_plate_detection.get_paddle_model()

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    img_bytes = await file.read()
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
    result=inferenceImage(
        number_plate_detection=number_plate_detection,
        yolo_model=yolo_model,
        original_image=img,
        text_conversion_model=text_conversion_model
    )
    return result

@app.post("/create-plate-data/plate_number/")
async def insert_plate(plate_number:str):
    # Insert the plate number into the database
    response = insert_vehicle_plate(plate_number)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return {"message": response["message"]}

@app.get("/checkNumberplate/plate_number")
async def checkNumberplate(plate_number: str):
    # Fetch the vehicle plate data from the database
    vehicle = check_number_plate_exist(plate_number)
    if not vehicle:
        raise HTTPException(status_code=404, detail=f"Vehicle with plate {plate_number} not found")
    result={"message":"number plate is validated"}
    return result
@app.get("/get-all-plates/")
async def get_all_plates():
    plates = get_all_vehicle_plates()
    if "error" in plates:
        raise HTTPException(status_code=400, detail=plates["error"])
    return {"plates": plates}


@app.put("/update-plate/{old_plate}/{new_plate}/")
async def update_plate(old_plate: str, new_plate: str):
    response = update_vehicle_plate(old_plate, new_plate)
    if "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    return {"message": response["message"]}


@app.delete("/delete-plate/{plate_number}/")
async def delete_plate(plate_number: str):
    response = delete_vehicle_plate(plate_number)
    if "error" in response:
        raise HTTPException(status_code=404, detail=response["error"])
    return {"message": response["message"]}


if __name__ == "__main__":
    # Run the FastAPI app with Uvicorn directly from the Python script
    uvicorn.run(app, host=api_host, port=api_port)
