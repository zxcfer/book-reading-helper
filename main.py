import os
import re
import tempfile

from google.cloud import storage, vision
from google.cloud import firestore

storage_client = storage.Client()
vision_client = vision.ImageAnnotatorClient()
db = firestore.Client()

def upload_book(data, context):
    file_data = data

    file_name = file_data['name']
    bucket_name = file_data['bucket']

    blob = storage_client.bucket(bucket_name).get_blob(file_name)
    blob_uri = f'gs://{bucket_name}/{file_name}'
    blob_source = {'source': {'image_uri': blob_uri}}

    if '.txt' not in file_name:
        print(f'The file {file_name} is not a book.')
        return

    print(f'Parsing {file_name}...')

    __save_book(blob)

def __save_book(current_blob):
    book = current_blob.download_as_string()

    # split file in paragraphs and clean empty ones
    paragraphs = re.split("\n\s*\n", book.decode("utf-8"))

    # clean paragraphs and save in firestore
    for i, p in enumerate(paragraphs):
        p_clean = p.strip()
        if p_clean != '':
            db.collection(u'books').document(current_blob.name).set(p_clean)

    print(f'Blurred image uploaded {file_name}')

def check_users_schedule():
    '''users [telegram_id, scheduled_start, scheduled_end, book, current_paragraph]
    '''
    # TODO find users scheduled to read in this time
    # TODO if yes find usdr_book and send paragrapsh

    pass


def __send_paragraphs(telegram_user_id, paragraphs):

    pass
