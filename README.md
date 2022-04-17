# Energy Hub - Building Energy Management Platform

Energy hub is an energy management platform that combines an interactive dashboard with deep learning and weather normalization models.

## :bookmark_tabs: Table of Contents
- [Introduction](#Introduction)
- [Description](#Description)
- [Dataset](#Dataset)
- [Live Demo](#demo)
- [Installation and Execution](#Installation)
- [Resources](#resources)

### :loudspeaker: Introduction

Global energy consumption is expected to reach `225,000` TWh in 2035. Buildings’ energy usage stands for approximately 40% of the global demand while generating 30% of the CO2 emissions. All of this requires energy management professionals to have the right tools to track energy KPIs for data driven energy optimization, carbon modeling, and budgeting. This holds especially true with world leaders’ commitment to limit global warming effects through the signing of the Paris Climate Accords, which aims to limit global warming to 1.5 degrees Celsius. The goal of this project is to develop an analytical web application for buildings’ energy management. This app presents interactive visualizations to summarize energy KPIs. It is powered by a machine-learning based energy benchmarking solution for energy deviation reporting, as well as deep learning models to provide mid-term energy forecast. 

### :information_source: Description
 
Our website is built using Dash Plotly framework and is made up of 4 main pages. In the home page we introduce the project and the team. Next, in the electricity modeling page we have a unique variety of filters that allows users to choose their aggregation level, chart duration, and which data elements to be shown on the charts among many other novel options. The goal is to allow users to compare electricity consumption of two buildings at a time. The other two pages allow the users to explore the energy usage of every building in the dataset per meter type and see the distribution of the primary/secondary usage for buildings in each site, as well as the average weather over 2016-2017 time period. All the pages are mobile friendly and can be viewed on mobile or tablet.

#### Main forecast page
<p float="left">
  <img src="webapp/assets/images/forecast_page.png">
</p>

#### Buildings' overview page
<p float="left">
  <img src="webapp/assets/images/building_page.png"> 
</p>

#### Sites overview page
<p float="left">
  <img src="webapp/assets/images/sites_overview.png">
</p>

### :file_folder: Dataset

Our dataset comes from The Building Data Genome Project 2, which can be downloaded from [here](https://github.com/buds-lab/building-data-genome-project-2). This dataset consists of 3,053 energy meters from 1,636 non-residential buildings in 19 sites across North America and Europe (see interactive map). The readings were recorded at one-hour intervals for electricity, chilled water, hot water, steam, irrigation and solar for 2016 and 2017. Buildings’ metadata includes year built, size, primary use, site, and source energy use intensity (EUI). Weather data (temperature, pressure, humidity, etc.) comes from the National Centers for Environmental Information database. Our dataset is approximately 2.6 GB in size, with nearly 53.6 million readings. 

The dataset is stored in Azure Data Lake

<p float="left">
  <img src="webapp/assets/images/azure.png">
</p>

### :movie_camera: Live Demo

You can view a live demo on this URL: https://energyhub.azurewebsites.net/

### :hammer: Installation and Execution

1. You need to download the webapp folder to your local machine and install the requirements by opening the folder in Command Line and Running: `pip install -r requirements.txt`
2. The data for this app is on Azure Data Lake Gen 2. You will need an Azure Account and you will need to create a Data Lake Storage Gen 2, Azure Key Vault, and Azure App Registration. see resources for useful links to get started .
3. Run the scripts under data_prep for preparing the dataset for modelling and visualization. These will upload data to ADLS.
4. Run the scripts the normalization and forecast scripts to generate the data files. Also Convert & Partition the cleaned meter readings files to parquet files using pandas. Forecast model must be ran for each site one at a time. These will upload model results to ADLS.
6. Head to the `data.py` file inside the web app folder to edit / update the locations of the files based on the structure you plan to have in your Data Lake.
7. Add Azure Client Secret, Client ID, and Tenant ID to your environment Variables.
8. Open the folder webapp inside any Pythong IDE, and then run  application.py . We reccomend Visual Studio Code, but you can use any other tool.
9. For your benefit, we have provided the below resources which can help you implement the above steps.


### :open_file_folder: Resources

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
