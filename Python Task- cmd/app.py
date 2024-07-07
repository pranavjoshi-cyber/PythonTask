import pandas as pd
from pymongo import MongoClient
import os

def upload_file(file_path):
    
    client = MongoClient('mongodb://localhost:27017/')
    db = client['python_db']
    collection = db['data']
    df = pd.read_excel(file_path)
    
    
    data_dict = df.to_dict("records")
    collection.insert_many(data_dict)
    print(f"Data from {file_path} successfully inserted into {db.name}.{collection.name}")

if __name__ == '__main__':
    file_path = input("Enter the path to the Excel file: ")

    print(f"Selected file: {file_path}")  
    if os.path.exists(file_path) and file_path.endswith(('.xlsx', '.xls')):
        try:
            upload_file(file_path)
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Invalid file path or file type. Please provide a valid Excel file.")
