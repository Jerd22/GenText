from exif import Image as ExifImage
from PIL import Image as PillowImage
from PIL import ExifTags
from pydantic import BaseModel
from typing import List
from json_tools import extract_json,validate_json_with_model,model_to_json,json_to_pydantic
from gemeni_generate import generate_text


pillow_img   = PillowImage.open("images/organ.jpg")
file_name = ""
class PromptModel(BaseModel):
    # Define your fields here, for example:
    details : str
    names : str
    keywords : List[str]

base_prompt = "Give this image 1 title and create 50 keywords with description for this image."
json_model = model_to_json(PromptModel(details="details", names="names", keywords=['keywords1', 'keywords2']))
optimized_prompt = base_prompt + f'.Please provide a response in a structured JSON format that matches the following model: {json_model}'

gemeni_response = generate_text(optimized_prompt,pillow_img)
print(gemeni_response)
json_objects = extract_json(gemeni_response)

validated, errors = validate_json_with_model(PromptModel, json_objects)

if errors:
    # Handle errors (e.g., log them, raise exception, etc.)
    
    print("Validation errors occurred:", errors)

else:
    model_object = json_to_pydantic(PromptModel, json_objects[0])
   
    #exif_dict = piexif.FocalLength(img.info["exif"])

    img_exif = pillow_img .getexif()
    keyword =  ';'.join(model_object.keywords)
    title = model_object.details
    
    img_exif[270] = str(title)
    img_exif[40091] = str(title).encode('utf-16')
    img_exif[40094] = keyword[:-1].encode('utf-16')
    img_exif[33432] = "Copyright 2022 Somchet Saengtawan. All Rights Reserved."

    file_name = model_object.names.replace(" ","_") + ".jpg"
    pillow_img.save(file_name, "jpeg", exif=img_exif)

