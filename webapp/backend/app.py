from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from azure_utils import KeyVault, DataLake
import pandas as pd

app = Flask(__name__)




@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')


@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')
   try:
      vault = KeyVault(keyVaultName = "keyvaultdva2022")
      storage_credential = vault.get_secret(secretName = "storagePrimaryKey")
      storage = DataLake(account_name = "storageaccountdva", credential = storage_credential)
      df = storage.read(file_system = "energyhub", directory = "/", file_name = "HassanTest.csv", extension = "csv")
      print(df)
   except Exception as e:
      name = e

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug=True)