from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

from azure_utils import KeyVault, DataLake


app = Flask(__name__)


@app.route('/')
def index():
   # vault = KeyVault(keyVaultName = "keyvaultdva2022")
   # storage_credential = vault.get_secret(secretName = "storagePrimaryKey")
   # storage = DataLake(account_name = "storageaccountdva", credential = storage_credential)
   # df = storage.read(file_system = "test", directory = "test", file_name = "test.csv", extension = "csv")
   # Adding a comment
   return render_template('index.html')


@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(debug=True)