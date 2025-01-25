import re 
from api.apivin import via_find
from AI.ocr.text_extracter import extract_text
from logger.logger_format import init_logger
import cv2
import numpy as np
import base64
import time
import traceback

def create_response_json(cropped_img,paddle_ocr,device_id,plate_data,im,stolen_list_number_plate,state_name,state_code,temp,stolen_list):
    try:
        
        json_sent_data =  {
                            "plate": "KL9094",
                            "stolen_count": 2,
                            "total_count": 5,
                            "stolen": 0,
                            "state" : state_name,
                            "make" : "Mercedes",
                            "model" : "C220",
                            "color" : "Gray",
                            "date_reported" : "01/24/2023",
                            "image":"",
                            "image_number_plate":""
                        }
        numpy_image = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
        ima2 = cv2.resize(numpy_image, (320, 163)).astype(np.float32)
        rotated_image = cv2.rotate(ima2, cv2.ROTATE_180)
        
        _, image_data = cv2.imencode(".jpg", im)
        # Encode the image data to base64
        image_base64 = base64.b64encode(image_data).decode("utf-8")
        
        
        _, image_data_plate = cv2.imencode(".jpg", cropped_img)
        # Encode the image data to base64
        image_base64_plate= base64.b64encode(image_data_plate).decode("utf-8")
       
        text=extract_text(rotated_image,paddle_ocr)
        print("orginal text",text)
        if text!="not detected" and text is not None:
            # print(text,"...................",temp)
           
            # if device_id in plate_data:print
            #     pass
            #     # print("#############################################",device_id,"#######",len(plate_data[device_id]))
            
            if text is not None and len(text) < 5:
                pass
            elif temp is not None and len(text)<len(temp) and text in temp:
                print("previous text came")
                pass
            elif temp is not None and len(text)==len(temp) and text==temp:
                print("previous text came")
                pass
            else:
                temp=text
                print("text ")
                if text is not None and len(text)>0:
                    # print("original text:     ",re.sub(r'[^a-zA-Z0-9]', '',text))
                    
                    if device_id not in plate_data.keys():
                        plate_data[device_id]=[text]
                    else:
                        value=plate_data[device_id]
                        value.append(text)
                        plate_data[device_id]=value
                    if  text in stolen_list:
                        text=re.sub(r'[^a-zA-Z0-9]', '',text)
                        # print("original text:     ",text)
                        
                        api_data=via_find(state_code,text)
                        if api_data["success"]:
                            # print("api success")
                            data=api_data["vin"]
                            # print("api data=",data)
                            vin=data["vin"]
                            year=data["year"]
                            make=data["make"]
                            car_model=data["model"]
                            color=data["color"]["name"]
                            json_sent_data["make"]=data["make"]
                            json_sent_data["model"]=data["model"]
                            json_sent_data["color"]=data["color"]["name"]
                        json_sent_data["stolen"]=1
                        if device_id not in stolen_list_number_plate.keys():
                            
                            stolen_list_number_plate[device_id]=[text]
                            # print("added numberplate to stolen list")
                        else:
                            value_stolen=stolen_list_number_plate[device_id]
                            value_stolen.append(text)
                            stolen_list_number_plate[device_id]=value_stolen
                    else:
                        json_sent_data["stolen"]=0
                    if device_id in stolen_list_number_plate:
                        json_sent_data["stolen_count"]= int(len(set(stolen_list_number_plate[device_id]))) 
                    if device_id in plate_data:
                        json_sent_data["plate"]=plate_data[device_id][-1]   
                        json_sent_data["total_count"]= int(len(set(plate_data[device_id]))) 
                    json_sent_data["image"]=image_base64
                    json_sent_data["image_number_plate"]=image_base64_plate

                    return json_sent_data,temp,True
        
        # temp="a"
        # print("did't get the response",temp)
        return json_sent_data,temp,False
    except Exception as e:
        # print(e)
        errors = str(traceback.format_exc())
        error_logger = init_logger("ERROR")
        error_logger.error(errors)