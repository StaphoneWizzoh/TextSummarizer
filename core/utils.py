import cohere
from PyPDF2 import PdfReader, PdfWriter
import os
import json
from django.conf import settings

base_dir = settings.BASE_DIR

with open(base_dir / 'env.json') as config_file:
    config = json.load(config_file)

def handle_upload(uploaded_file):
  file_path = os.path.join(base_dir + uploaded_file.name)
  
  with open(file_path, 'wb') as destination:
    for chumk in uploaded_file.chunks():
      destination.write(chunk)
      
  return file_path

def extract_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
      pdf = PdfReader(f)
      text = ""
      for page in pdf.pages:
        
        page_text = page.extract_text()
        text += page_text + "\n"
      with open('sample.txt', 'w') as f:
        f.write(text)
        
      return text
  
def summarizer(text_string):
    co = cohere.Client(config['COHERE_API_KEY'])
    response = co.summarize(
        text=text_string,
    )
    return response.summary
  
def extract_and_generate(pdf_path):
  text = extract_pdf(pdf_path)
  summary = summarizer(text)
  return summary
    
    
# def generate_pdf(text,output_file_path):
#   pdf_writer = PdfWriter()
#   pdf_page = pdf_writer.add_page()
#   pdf_page.setFont("Calibri", 14)
#   lines = text.split('\n')
#   y_position = 840 * 2
  
#   for line in lines:
#     pdf_page.drawString(100,y_position, line)
#     y_position -= 14
    
#   with open(output_file_path, 'w') as output_file:
#     pdf_writer.write(output_file)

def generate_pdf(text, destination_path):
  pdf_writer = PdfWriter()
  pdf_page = pdf_writer.add_page()
  pdf_page.set_font("Calibri", size=12)
  pdf_page.cell(200,10, txt=text, ln=True)
  
  with open(destination_path, 'wb') as pdf_file:
    pdf_writer.output(pdf_file)