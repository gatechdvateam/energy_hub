# Energy Hub - Building Energy Management Platform

## About the project
Energy hub is an energy management platform that combines visual interactive dashboard with deep learning and weather normalization models.

## Live Demo
You can view a live demo on this URL: https://energyhub.azurewebsites.net/.


## How to start a local demo:
1- You need to download the webapp folder to your local machine and install the requirements by opening the folder in Command Line and Running: pip install -r requirements.txt


2- The data for this app is on Azure Data Lake Gen 2. You will need an Azure Account and you will need to create a Data Lake Storage Gen 2, Azure Key Vault, and Azure App Registration. Below articles may help you:

https://docs.microsoft.com/en-us/learn/modules/create-an-azure-account/

https://docs.microsoft.com/en-us/azure/storage/blobs/create-data-lake-storage-account

https://docs.microsoft.com/en-us/azure/key-vault/general/quick-create-portal

https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app



3- Run the scripts the normalization and forecast scripts to generate the data files. Also Convert & Partition the cleaned meter readings files to using pandas.
https://stackoverflow.com/questions/52934265/how-to-write-a-partitioned-parquet-file-using-pandas

https://pandas.pydata.org/pandas-docs/version/1.1/reference/api/pandas.DataFrame.to_parquet.html


4- Upload the data to Azure Storage Account


5- Head to the data.py file inside the web app folder to edit / update the locations of the files based on the structure you plan to have in your Data Lake.


6- Add Azure Client Secret, Client ID, and Tenant ID to your environemnt Variables.


7- Run the app.
