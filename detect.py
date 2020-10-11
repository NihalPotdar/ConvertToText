import os
import json
import re
import argparse

# Imports the Google Cloud client library
from google.cloud import vision
from write_to_excel import write

client = vision.ImageAnnotatorClient()
parser = argparse.ArgumentParser(description='Transcribe to an excel file')
parser.add_argument('--folder-path', type=str, help='the path of the folder with images on the local directory', required=True)
parser.add_argument('--csv-path', type=str, help='the name or path of the csv file to be created')
args = parser.parse_args()

data_rows = []

patterns = {
    "receipt": "Receipt[ :][0-9][0-9][0-9][0-9]",
    "date":  r"^(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])$ | \w+\s\d+(st)?(nd)?(rd)?(th)?,\s+\d+ | \d{4}[-/ ]\d{2}[-/ ]\d{2}",
    "recieved_name": r"Received With Thanks From:[ a-zA-Z]*(Address)*",
    "address": r"Address[a-zA-Z0-9,.() ]*Ph | [0-9]+[a-zA-Z,.() ]*NW | [0-9]+[a-zA-Z,.() ]*SW | [0-9]+[a-zA-Z,.() ]*NE | [0-9]+[a-zA-Z,.() ]*SE | \s*([0-9]*)\s((NW|SW|SE|NE|S|N|E|W))?(.*)((NW|SW|SE|NE|S|N|E|W))?((#|APT|BSMT|BLDG|DEPT|FL|FRNT|HNGR|KEY|LBBY|LOT|LOWR|OFC|PH|PIER|REAR|RM|SIDE|SLIP|SPC|STOP|STE|TRLR|UNIT|UPPR|\,)[^,]*)(\,)([\s\w]*)\n",
    "phone_number": r"\d{3}[-\.\s]??\d{3}[-\.\s]??\d{3,4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{3,4}|\d{3}[-\.\s]??\d{3,4}",
    "amount": "\$[ _\d]*"
}
special_conditions = {
    "recieved_name": ["Received With Thanks From", "Address"],
    "address": ["Ph"],
    "phone_number": ['Ph'],
    "amount": ["$"],
    "date": ["Received"]
}
duplicate_number = '(403) 668-0653'

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
        
        if col == "phone_number":
            extend = re.findall(patterns[col], text)
            entry = ""
            for i in extend:
                if i == duplicate_number:
                    continue
                elif '403' in i or '587' in i:
                    entry = i
        else:
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

    print(data) # test
    data_rows.append(list(data.values()))

if __name__ == '__main__':
    folder_path = args.folder_path
    csv_path = args.csv_path
    
    #detect_document(os.path.join(folder_path, 'np.jpg'))
    for image_path in os.listdir(folder_path):
        detect_document(os.path.join(folder_path, image_path))
        data = {}

    write(csv_path, data_rows)