import os
import pandas as pd
from fastapi import UploadFile

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_and_parse_file(file: UploadFile):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())
    # Parse file with pandas
    if file.filename.endswith('.csv'):
        df = pd.read_csv(file_location)
    elif file.filename.endswith(('.xls', '.xlsx')):
        df = pd.read_excel(file_location)
    else:
        raise ValueError("Unsupported file type")
    return file_location, df
