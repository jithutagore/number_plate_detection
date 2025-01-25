from AI.yolov5.model_load import load_model
import numpy as np
import cv2
from AI.yolov5.detect import run
import pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
from AI.ocr.PaddleOCR.paddleocr import PaddleOCR
from AI.ocr.text_extracter import extract_text

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

