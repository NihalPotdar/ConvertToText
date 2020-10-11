import os
import json
import re
import argparse

# Imports the Google Cloud client library
from google.cloud import vision
import write_to_excel

client = vision.ImageAnnotatorClient()
parser = argparse.ArgumentParser(description='Transcrible to an excel file')
parser.add_argument('--folder-path', type=str, help='the path of the folder with images on the local directory', required=True)
parser.add_argument('--csv-path', type=str, help='the name or path of the csv file to be created')
args = parser.parse_args()

data_rows = []

patterns = {
    "receipt": "Receipt[ :][0-9][0-9][0-9][0-9]",
    "date":  "Date.*Received",
    "recieved_name": "Received With Thanks From.*Address",
    "address": "Address.*Ph",
    "phone_number": "Ph[ :]+[ \d-]*",
    "amount": "\$[_\d]*"
}
special_conditions = {
    "recieved name": ["Received With Thanks From", "Address"],
    "address": ["Ph"],
    "phone_number": ['Ph'],
    "amount": ["$"],
    "date": ["Received"]
}

data = {}

def detect_document(path):
    with open(path, "rb") as image_file:
        content = image_file.read()

    response = client.document_text_detection(image=vision.Image(content=content))

    '''
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            print('\nBlock Confidence: {}\n'.format(
                block.confidence
            ))

            for paragraph in block.paragraphs:
                print(f'Paragraph confidence: {paragraph.confidence}')

                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    print(f'Word text: {word_text} (confidence: {word.confidence})')
        '''
    
    text = response.full_text_annotation.text
    text = text.replace("\n", " ")
    print(text) # test
    
    for col in patterns:
        entry = re.search(patterns[col], text)
    
        try:
            entry = entry.group()
        except:
            entry = ""

        if col in special_conditions:
            for i in special_conditions[col]:
                entry = entry.replace(i, "")

        data[col] = entry.lower().replace(col, "").replace(":", "").replace("_", "").strip()

        if col == "recieved name" and ('inc' in data[col] or 'ltd' in data[col]):
            data['additional comments'] = 'corp'

    data_rows.append(list(data.values()))

if __name__ == '__main__':
    folder_path = args.folder_path
    csv_path = args.csv_path
    print(folder_path)
    print(csv_path)
    
    for image_path in os.listdir(folder_path):
        detect_document(os.path.join(os.getcwd(), "test22.jpg"))