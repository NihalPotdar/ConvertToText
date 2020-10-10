import os
# Imports the Google Cloud client library
from google.cloud import vision
client = vision.ImageAnnotatorClient()

def detect_document(path):
    with open(path, "rb") as image_file:
        content = image_file.read()

    response = client.document_text_detection(image=vision.Image(content=content))
    print("response: " +  str(response))

if __name__ == '__main__':
    detect_document(os.path.join(os.getcwd(), "detect.py"))