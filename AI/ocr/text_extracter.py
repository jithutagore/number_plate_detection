import numpy as np
import cv2
import time
import re
import torch
import traceback

def extract_text(image, ocr):
    try:
        result = ocr.ocr(image, cls=True)
        if len(result[0]) != 0:
            result = sorted(result, key=lambda x: x[0][0][0])
            detected_text = ""
            max_area = 0
            area = 0
            area_dict = {}
            confidence_dict = {}
            for res in result:
                for line in res:
                    detected_text = line[1][0]
                    confidence = line[1][1]
                    if confidence > 0.8:
                        length = np.sum(np.subtract(line[0][1], line[0][0])) * 6
                        height = np.sum(np.subtract(line[0][2], line[0][1])) * 6
                        area = length * height
                        if area > max_area:
                            max_area = area
                        area_dict[detected_text] = area
                        confidence_dict[detected_text] = confidence  # Store the confidence
            print(area_dict)
            texts_above_threshold = [text for text, area in area_dict.items() if area / max_area > 0.85]
            confidences_above_threshold = [confidence_dict[text] for text in texts_above_threshold]  # Get corresponding confidences
            output_text = " ".join(texts_above_threshold)

            return output_text, confidences_above_threshold  # Return text and confidences
        else:
            no_value = "not detected"
            return no_value, []  # Return "not detected" with empty confidence list
    except RuntimeError as e:
        # Handle the error
        print(f"An error occurred: {e}")
        traceback.print_exc()
        torch.cuda.empty_cache()
        paddle.fluid.core._reset_tensor_lod()
    except Exception as e:
        print(e)
        traceback.print_exc()