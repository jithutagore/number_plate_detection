from AI.yolo.model_load import load_model
import numpy as np
import cv2
from AI.yolov5.detect import run
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
from AI.ocr.PaddleOCR.paddleocr import PaddleOCR

class NumberPlateDetection:
    def __init__(self):
        # Ensure weights and data paths are passed as strings
        self.model, self.stride, self.names, self.pt = load_model(
            weights="AI\\model\\detection\\number_plate_detection_model.pt", 
            data="AI\\model\\detection\\coco.yaml"
        )
        self.paddle_ocr = PaddleOCR(det_model_dir="AI/ocr/ch_ppocr_mobile_v2.0_det_infer", 
                                    rec_model_dir="AI/ocr/ch_ppocr_mobile_v2.0_rec_infer", 
                                    cls_model_dir="AI/ocr/ch_ppocr_mobile_v2.0_cls_infer", 
                                    use_angle_cls=True, lang='en', use_gpu=True)
    
    def get_yolo_model(self):
        return self.model, self.stride, self.names, self.pt
    
    def preprocess_image(self, image):
        # Resize the image and prepare it for YOLO detection
        resized_image = cv2.resize(image, (640, 352))
        final_image = np.transpose(resized_image, (2, 0, 1))
        return final_image
    def get_paddle_model(self):
        return self.paddle_ocr

# Load the image
img = cv2.imread("1.png")

# Initialize the NumberPlateDetection class
number_plate_detection = NumberPlateDetection()

# Get YOLO model components
model, stride, name, pt = number_plate_detection.get_yolo_model()
text_conversion_model = number_plate_detection.get_paddle_model()

# Preprocess the image
resized_image = number_plate_detection.preprocess_image(image=img)

# Run YOLO detection
detected_image = run(model=model, original_image=img, finale=resized_image)

numberplate_value=text_conversion_model.ocr(detected_image, cls=True)
if len(numberplate_value[0])!=0:
    result=sorted(numberplate_value, key =lambda x:x[0][0][0])
    detected_text = ""
    max_area=0
    area=0
    area_dict = {}
    for res in result:
        for line in res:
            detected_text = line[1][0]
            confidence=line[1][1]
            print("text===========",detected_text,"con==========",confidence)
# Save the resulting image
cv2.imwrite("croppedimage.png", detected_image)
