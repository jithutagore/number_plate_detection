import time
from AI.ocr.text_extracter import extract_text
from AI.yolov5.detect import run
from loggerSetup import logger
from traffiicDbOperation import check_number_plate_exist
from fastapi import HTTPException
import re

# Function to preprocess the image
def preprocess_image(number_plate_detection, original_image):
    resized_image = number_plate_detection.preprocess_image(image=original_image)
    return resized_image

# Function to run YOLO model for number plate detection
def detect_number_plate(yolo_model, original_image, resized_image):
    detection_start_time = time.time()  
    detected_image, yolo_detection_confidence = run(model=yolo_model, original_image=original_image, finale=resized_image)
    detection_end_time = time.time()  
    logger.info(f"YOLO detection time in seconds %f", detection_end_time - detection_start_time)
    logger.info("YOLO detection confidence: %f", yolo_detection_confidence)
    
    return detected_image, yolo_detection_confidence

# Function to perform OCR on the detected image
def extract_number_plate_text(detected_image, text_conversion_model):
    ocr_start_time = time.time() 
    numberplate_value, ocr_confidence = extract_text(image=detected_image, ocr=text_conversion_model)
    ocr_end_time = time.time()  
    logger.info("OCR extraction time in seconds: %f", ocr_end_time - ocr_start_time)
    logger.info("Extracted number plate value is: %s", numberplate_value)
    
    return numberplate_value, ocr_confidence

# Function to check if the number plate exists in the database
def validate_number_plate(numberplate_value):
    ifNumberPlateExist = check_number_plate_exist(plate_number=numberplate_value)
    return ifNumberPlateExist

# Function to handle the main inference process
def inferenceImage(number_plate_detection, yolo_model, original_image, text_conversion_model):
    start_time = time.time()
    
    # Preprocess the image
    resized_image = preprocess_image(number_plate_detection, original_image)
    
    # Detect number plate using YOLO
    detected_image, yolo_detection_confidence = detect_number_plate(yolo_model, original_image, resized_image)
    
    if yolo_detection_confidence < 0.7:
        logger.info("No number plate found in image")
        raise HTTPException(status_code=404, detail="No number plate detected in the image")

    # Extract text from the detected image
    numberplate_value, ocr_confidence = extract_number_plate_text(detected_image, text_conversion_model)
    plate_number_clean = re.sub(r'[^A-Za-z0-9]', '', numberplate_value)
    
    if len(ocr_confidence) > 0 and ocr_confidence[0] < 0.8 or len(ocr_confidence) == 0:
        logger.info("Number plate image is unclear")
        raise HTTPException(status_code=400, detail="Number plate not clear image")

    # End total inference time
    end_time = time.time()
    logger.info(f"Total inference time in seconds: %f", end_time - start_time)
    
    # Validate if number plate exists
    ifNumberPlateExist = validate_number_plate(plate_number_clean)
    
    if ifNumberPlateExist:
        return {
            "message": "Number plate extraction successful and validated",
            "response": {
                "numberplate": plate_number_clean,
                "yolo_accuracy": yolo_detection_confidence,
                "image_to_text_accuracy": ocr_confidence[0],
                "response_time": end_time - start_time
            }
        }
    if not ifNumberPlateExist:
        return {
            "message": "Number plate extraction successful and not validated",
            "response": {
                "numberplate": plate_number_clean,
                "yolo_accuracy": yolo_detection_confidence,
                "image_to_text_accuracy": ocr_confidence[0],
                "response_time": end_time - start_time
            }
        }
