from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from pymongo import MongoClient
import os

client = MongoClient('mongodb://localhost:27017/')
db_name = 'python_db'  
collection_name = 'data'  


app = Flask(__name__)  # initializing flask here
app.secret_key = 'secret_key'


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
       
        if 'file' not in request.files:
            flash('No file')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and file.filename.endswith(('.xlsx', '.xls')):
            try:
                df = pd.read_excel(file)
                db = client[db_name]
                collection = db[collection_name]
                data_dict = df.to_dict("records")
                collection.insert_many(data_dict)
                
                flash(f"The file {file.filename} is inserted into {db_name}.{collection_name}")
            except Exception as e:
                flash(f"An error occurred: {str(e)}")
            
            return redirect(url_for('upload_file'))
        else:
            flash('Invalid file type. Please upload a valid Excel file.')
            return redirect(request.url)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
