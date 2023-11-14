import cohere
from PyPDF2 import PdfReader, PdfWriter
import os
import json
from django.conf import settings
from reportlab.pdfgen import canvas

base_dir = settings.BASE_DIR

with open(base_dir / 'env.json') as config_file:
    config = json.load(config_file)

def handle_upload(uploaded_file):
  file_path = os.path.join(base_dir + uploaded_file.name)
  
  with open(file_path, 'wb') as destination:
    for chunk in uploaded_file.chunks():
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
    
    
def create_pdf(input_text,output_path):
  pdf_canvas = canvas.Canvas(output_path)
  pdf_canvas.setFont("Helvetica", 12)
  lines = input_text.split("\n")
  y_position = 750
  
  for line in lines:
    pdf_canvas.drawString(100, y_position, line)
    y_position -= 15
    
  pdf_canvas.save()
  return