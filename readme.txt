Live Demo

You can view a live demo on this URL: https://energyhub.azurewebsites.net/

Description
 
Our website is built using Dash Plotly framework and is made up of 4 main pages. In the home page we introduce the project and the team. Next, in the electricity modeling page we have a unique variety of filters that allows users to choose their aggregation level, chart duration, and which data elements to be shown on the charts among many other novel options. The goal is to allow users to compare electricity consumption of two buildings at a time. The other two pages allow the users to explore the energy usage of every building in the dataset per meter type and see the distribution of the primary/secondary usage for buildings in each site, as well as the average weather over 2016-2017 time period. All the pages are mobile friendly and can be viewed on mobile or tablet.

Sample images of the website can be found in the below folders:
webapp/assets/images/forecast_page.png
webapp/assets/images/building_page.png
webapp/assets/images/building_page.png
webapp/assets/images/sites_overview.png

Dataset

Our dataset comes from The Building Data Genome Project 2, which can be downloaded from [here](https://github.com/buds-lab/building-data-genome-project-2). This dataset consists of 3,053 energy meters from 1,636 non-residential buildings in 19 sites across North America and Europe (see interactive map). The readings were recorded at one-hour intervals for electricity, chilled water, hot water, steam, irrigation and solar for 2016 and 2017. Buildings’ metadata includes year built, size, primary use, site, and source energy use intensity (EUI). Weather data (temperature, pressure, humidity, etc.) comes from the National Centers for Environmental Information database. Our dataset is approximately 2.6 GB in size, with nearly 53.6 million readings. 

The dataset is stored in Azure Data Lake. The image and the python file in the below folders will help you understand the required data structure. They are mentioned here for your benefit.

webapp/assets/images/azure.png
webapp/data.py


Installation and Execution

1. You need to download the webapp folder to your local machine and install the requirements by opening the folder in Command Line and Running: `pip install -r requirements.txt`

2. The data for this app is on Azure Data Lake Gen 2. You will need an Azure Account and you will need to create a Data Lake Storage Gen 2, Azure Key Vault, and Azure App Registration. see resources for useful links to get started .

3. Run the scripts under data_prep for preparing the dataset for modelling and visualization. These will upload data to ADLS.

4. Run the scripts the normalization and forecast scripts to generate the data files. Also Convert & Partition the cleaned meter readings files to parquet files using pandas. Forecast model must be ran for each site one at a time. These will upload model results to ADLS.

6. Head to the `data.py` file inside the web app folder to edit / update the locations of the files based on the structure you plan to have in your Data Lake.

7. Add Azure Client Secret, Client ID, and Tenant ID to your environment Variables.

8. Open the folder webapp inside any Pythong IDE, and then run  application.py . We reccomend Visual Studio Code, but you can use any other tool.

webapp/application.py

9. For your benefit, we have provided the below resources which can help you implement the above steps.


Resources

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
