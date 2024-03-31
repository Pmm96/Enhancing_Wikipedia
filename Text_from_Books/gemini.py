import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown


def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


# Or use `os.getenv('GOOGLE_API_KEY')` to fetch an environment variable.
GOOGLE_API_KEY='AIzaSyAraI1HokPy4ZGBbCxNWeq_ugQ7TOuMizs'
genai.configure(api_key=GOOGLE_API_KEY)


import os
import fitz 
from IPython.display import Image
from IPython.core.display import HTML
import time

model = genai.GenerativeModel('gemini-1.5-pro-latest')
Nprompt = "You are given an Image from a scanned page of a textbook. Get all the text from it as it is. Do not explain anything. Also do not add any extra information.If there is no text in the image, then do not return.'#_NO_TEXT' "
person = "Jessie_Ackermann"

def extract_images_from_pdf(pdf_path, image_folder, txt_folder):
    os.makedirs(image_folder, exist_ok=True)
    os.makedirs(txt_folder, exist_ok=True)  # Create the text folder if it doesn't exist
    
    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):
        if page_number <= 17:
            continue
        
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap()

        image_path = f"{image_folder}/page_{page_number + 1}.png"

        image.save(image_path)
        img = Image(image_path)  # Corrected variable name

        response = model.generate_content([Nprompt, img], stream=True)
        response.resolve()
        gentxt = response.text

        txt_path = f"{txt_folder}/page_{page_number + 1}.txt"
        with open(txt_path, "w") as txt_file:
            txt_file.write(gentxt)
            
        time.sleep(40)    

    pdf_document.close()
    
    
    


# Example usage
# %cd "/home/pauras-am/Text_from_Books"
pdf_path = "./Books/worldthroughwoma00acke_bw.pdf" 
image_folder = "./Images/" + person
txt_folder = "./Text/" + person
extract_images_from_pdf(pdf_path, image_folder,txt_folder)











    