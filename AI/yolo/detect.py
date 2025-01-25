import os
import sys
from pathlib import Path
import numpy as np
import torch
import traceback
from AI.ocr.text_extracter import extract_text

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from utils.general import (cv2, non_max_suppression, scale_boxes)

def run(paddle_ocr, device_id, plate_data,stolen_dict_number_plate, state_name, state_code, stolen_list,temp_plate,model,stride,names,pt,device,original_image,finale,connection="",
        imgsz=(640, 640), 
        conf_thres=0.1, 
        iou_thres=0.01,  
        max_det=1000,  
        save_crop=False,  
        
        classes=None,  
        agnostic_nms=False,  
        augment=False,  
        visualize=False,  
        line_thickness=3,  
        vid_stride=1
):
    try:  
      
        im = torch.from_numpy(finale).to(model.device)
        im = im.half() if model.fp16 else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # expand for batch dim
        
        pred = model(im, augment=augment, visualize=visualize)
        
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)
        
        if len(pred[0])>0:
            for i, det in enumerate(pred):  # per image
                # seen += 1
          
                if len(det):
                    # Rescale boxes from img_size to im0 size
                    det_array=det.detach().cpu().numpy()
                    for each_value in  det_array:
                        height,width,ch=original_image.shape
                        x1=int((each_value[0]/640)*width)
                        y1=int((each_value[1]/352)*height)
                        x2=int((each_value[2]/640)*width)
                        y2=int((each_value[3]/352)*height)
                        confidence=float(each_value[4])
                        cls=int(each_value[5])
                        if cls==0:
                            cropped_img = original_image[y1:y2, x1:x2]
                            text=extract_text(cropped_img,paddle_ocr)
                            # print(type(cropped_img),cropped_img.shape)
                            # cv2.imwrite("inf/cropped"+str(confidence)+".png",cropped_img) 
                            # print("ok")

                            # return cropped_img   
                                      
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc() 
    except RuntimeError as e:
        # Handle the error
        print(f"An error occurred: {e}")
        traceback.print_exc()
                               
                            
                
