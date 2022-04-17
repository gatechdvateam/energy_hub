# Energy Hub: Building an Energy Management Platform

Energy hub is an energy management platform that combines an interactive dashboard with the state of the art deep learning transformers architecture and online machine learning models for weather normalization purposes

### Live Demo

The app is deployed on Azure websites and can be viewed at https://energyhub.azurewebsites.net/

### Description
 
Our website is built using Dash Plotly framework and is made up of 4 main pages. In the home page we introduce the project and the team. Next, in the electricity modeling page we have a unique variety of filters that allows users to choose their aggregation level, chart duration, and which data elements to be shown on the charts among many other novel options. The goal is to allow users to compare electricity consumption of two buildings at a time. The other two pages allow the users to explore the energy usage of every building in the dataset per meter type and see the distribution of the primary/secondary usage for buildings in each site, as well as the average weather over 2016-2017 time period. All the pages are mobile friendly and can be viewed on mobile or tablet.

Sample images of the website can be found in the below folders:
	- webapp/assets/images/forecast_page.png
	- webapp/assets/images/building_page.png
	- webapp/assets/images/building_page.png
	- webapp/assets/images/sites_overview.png

### Dataset

Our dataset comes from The Building Data Genome Project 2, which can be downloaded from [here](https://github.com/buds-lab/building-data-genome-project-2). This dataset consists of 3,053 energy meters from 1,636 non-residential buildings in 19 sites across North America and Europe (see interactive map). The readings were recorded at one-hour intervals for electricity, chilled water, hot water, steam, irrigation and solar for 2016 and 2017. Buildings’ metadata includes year built, size, primary use, site, and source energy use intensity (EUI). Weather data (temperature, pressure, humidity, etc.) comes from the National Centers for Environmental Information database. Our dataset is approximately 2.6 GB in size, with nearly 53.6 million readings. 

The dataset is stored in Azure Data Lake. The image and the python file in the below folders will help you understand the required data structure. 
- webapp/assets/images/azure.png
- webapp/data.py


#### Installation Requirements

	* Download an IDE. We highly recommend VScode
	* Download `Python-3.9.11` [here](https://www.python.org/ftp/python/3.9.11/python-3.9.11-amd64.exe)
	* Create an Azure account, a Data Lake Storage Gen 2 account, Azure Key vault, and Azure Webapp registration account (see resources)
	* Add Azure Client Secret key, Client ID, and Tenant ID to your environment variables

### Installation and Execution

1. In the project folder, create a virtual environment using the following steps:
	* Open GitBash or Command prompt
	* Run:  `py -m venv .venv`
	* Run: `source .venv\Scripts\activate
	* Install requirements:  `pip install -r requirements.txt`
	
2. Run the notebooks in the **"data_prep"** folder which will prep the data and upload it to Azure Data Lake Storage

	* execute `meta_weather_clean.ipynb`
	* execute `meters_clean.ipynb`
	
3. Run the notebooks in both **"forecast"** and **"normalization"** folders

	* Note: Forecast model must be ran for each site one at a time and the model results will upload to Azure storage automatically
	
4. Convert & Partition the cleaned meter readings files to parquet files using pandas. The `webapp/partitionParqs.py` will help you do that

6. Update the `data.py`  under **webapp** folder to follow your folder structure in Azure

8. Go to **webapp** folder in your command line

	* Run `code .` to open a vscode code in the folder
	* In your command line, run `python application.py`
	* Dash will open a localhost address for you in the command line, follow the link


### Resources

* Set up a Azure account
	* [Azure account](https://docs.microsoft.com/en-us/learn/modules/create-an-azure-account/)
	
* Create a data lake account
	* [Data Lake](https://docs.microsoft.com/en-us/azure/storage/blobs/create-data-lake-storage-account)

*  Create a key vault using the Azure portal
	* [Key Vault](https://docs.microsoft.com/en-us/azure/key-vault/general/quick-create-portal)
	
* Register an application
	* [Register App](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)

* How to write a partitioned Parquet file using Pandas
	* [Parquet file using Pandas](https://stackoverflow.com/questions/52934265/how-to-write-a-partitioned-parquet-file-using-pandas)

* Write a DataFrame to the binary parquet format
	* [Convert Pandas Dataframe to parquet](https://pandas.pydata.org/pandas-docs/version/1.1/reference/api/pandas.DataFrame.to_parquet.html)


