
#This is our Color palette for all charts. Change it or define your own here.
ColorPalette = ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]

PrimaryUsageMarkDown = '''
#### What is Lorem Ipsum?

Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
 when an unknown printer took a galley of type and scrambled it to make a type
  specimen book. It has survived not only five centuries, but also the leap into 
  electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages,
 and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
'''

random_text = '''

Global energy consumption is expected to reach `225,000 TWh` in `2035`.
Buildings’ energy usage stands for approximately **40%** of the global demand while generating **30%** of the CO2 emissions.
All of this requires energy management professionals to have the right tools to track energy KPIs for data driven energy optimization, carbon modeling, and budgeting.
This holds especially true with world leaders’ commitment to limit global warming effects through the signing of the Paris Climate Accords, which aims to limit global warming to 1.5 degrees Celsius.
The goal of this project is to develop an analytical web application for buildings’ energy management. 
This app presents interactive visualizations to summarize energy KPIs. 
It is powered by a machine-learning based energy benchmarking solution for energy deviation reporting, as well as deep learning models to provide mid-term energy forecast. 

#### Why does it matter?

Energy efficiency in residential and commercial buildings heavily rely on how the buildings operate.
A real-time energy management platform is crucial in ensuring a degree of efficiency when it comes to commercial buildings' energy operations.
Energy operations usually have some degree of uncertainty that can be attributed to several factors:
 - 1. The accuracy of the energy consumption forecasting models used,
 - 2. weather fluctuations, and 
 - 3. the adoption of poor practices in building operations.

According to a study conducted by Liping Wang et al across four different cities (Washington DC, San Francisco, Atlanta, and Chicago),
poor practices in buildings’ operations across multiple parameters resulted
in an increase in energy usage of `49-79%`, where HVAC operations was the most influential with `-15.3% to 70.3%` 
variation in annual site energy consumption. While good practices led to a reduction in energy usage by `15% to 29%` across these cities.
An energy management platform like ours will provide insight into to how energy resources are being used, 
providing the necessary data to adopt better operational practices such as lighting control, occupancy-based HVAC scheduling, etc.


#### Dataset

Our dataset comes from *The Building Data Genome Project 2*.
This dataset consists of 3,053 energy meters from `1,636` non-residential buildings in `19` sites across North America and Europe (see interactive map). 
The readings were recorded at one-hour intervals for electricity, chilled water, hot water, steam, irrigation and solar for **2016 and 2017**.
Buildings’ metadata includes year built, size, primary use, site, and source energy use intensity (EUI). Weather data (temperature, pressure, humidity, etc.) 
comes from the National Centers for Environmental Information database.
Our dataset is approximately `2.6 GB` in size, with nearly `53.6` million readings

'''

TEAM_TEXT_STYLE = {
    'color': 'black',
    'font-family': 'serif',
    'font-size': '25px'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': 'black',
    'font-size':'20px'
}

TEXT_STYLE = {
    'color': '#191970',
    'font-family': 'serif',
    'font-size': '18px'
}

TEAM_HEADING_STYLE = {
    'color': '#191970',
    'font-family': 'serif',
    'font-size':'40px'
}

CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}


STATS_CARD =  {
            'display': 'inline-block',
            'text-align': 'center',
            'color':'black',
            'font-size':'25px'
           }
           
HomePageIntro = '''
# Energy Hub
## A futuristic energy consumption dashboard
### To-do: add more tex.
'''