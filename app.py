from exif import Image as ExifImage
from PIL import Image as PillowImage
from PIL import ExifTags
from pydantic import BaseModel
from typing import List
from json_tools import extract_json,validate_json_with_model,model_to_json,json_to_pydantic
from gemeni_generate import generate_text
import csv
import os
import datetime

#pillow_img   =  PillowImage.open("images/images_1.jpg")
directory_form = ""
file_name = ""
directory_to = ""
list_json = []

class PromptModel(BaseModel):
    # Define your fields here, for example:
    Title : str
    Filename : str
    Category : str
    Releases : str
    Keywords : List[str]

base_prompt = "Give this image 1 title and create 50 keywords with description for this image."
json_model = model_to_json(PromptModel(Title="Title", Filename="Filename",Category="Category", Releases="Releases", Keywords=['Keywords1', 'Keywords2']))

def GetPrompt(img):      
    optimized_prompt = base_prompt + f'.Please provide a response in a structured JSON format that matches the following model: {json_model}'
    gemeni_response = generate_text(optimized_prompt,img)
    json_objects = extract_json(gemeni_response)
    return json_objects

def Write_file(data):
    today = datetime.datetime.now()
    filename = "Keywords_{}.csv".format(data)
    filePath = os.path.join(directory_to, filename)
    if not os.path.exists(directory_to):
        os.makedirs(directory_to)

    fileExists = os.path.isfile(filePath)
    if not fileExists:
        with open(filePath, 'a') as csvfile:
            write = csv.writer(csvfile, lineterminator='\n')
            write.writerow([list_json])

    
directory = os.fsencode(directory_form)
for img in os.listdir(directory):  
    if img.endswith(".jpg") or img.endswith(".png"):
        PillowImage.open(img)
        promp = GetPrompt(img)
        validated, errors = validate_json_with_model(PromptModel, promp)
        if not errors:
            m_object = json_to_pydantic(PromptModel, promp[0])
            file_name = m_object.Filename.replace(" ","_") + ".jpg"
            keyword =  ';'.join(m_object.Keywords)[:-1].encode('utf-16')
            title = m_object.Title
            release = m_object.Releases
            rategory = m_object.Category

            list_json.append({
                "Filename" : file_name,
                "Title" : m_object.Title,
                "Keywords" : keyword,
                "Category": m_object.Category,
                "Releases": m_object.Releases,
            })

            img_exif = img.getexif()

            img_exif[270] = str(title)
            img_exif[40091] = str(title).encode('utf-16')
            img_exif[40094] = keyword
            img_exif[33432] = "Copyright 2022 Somchet Saengtawan. All Rights Reserved."

            img.save( os.path.join(directory_to, file_name) , "jpeg", exif=img_exif)



