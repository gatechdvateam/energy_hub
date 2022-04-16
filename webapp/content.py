
#This is our Color palette for all charts. Change it or define your own here.
ColorPalette = ["#b30000", "#7c1158", "#4421af", "#1a53ff", "#0d88e6", "#00b7c7", "#5ad45a", "#8be04e", "#ebdc78"]

INTRO_TEXT = '''
Global energy consumption is expected to reach `225,000 TWh` in `2035`.
Buildings’ energy usage stands for approximately **40%** of the global demand while generating **30%** of the CO2 emissions.
All of this requires energy management professionals to have the right tools to track energy KPIs for data driven energy optimization, carbon modeling, and budgeting.
This holds especially true with world leaders’ commitment to limit global warming effects through the signing of the Paris Climate Accords, which aims to limit global warming to 1.5 degrees Celsius.
The goal of this project is to develop an analytical web application for buildings’ energy management. 
This app presents interactive visualizations to summarize energy KPIs. 
It is powered by a machine-learning based energy benchmarking solution for energy deviation reporting, as well as deep learning models to provide mid-term energy forecast. 

#### Dataset

Our dataset comes from *The Building Data Genome Project 2*.
This dataset consists of `3,053` energy meters from `1,636` non-residential buildings in `19` sites across North America and Europe (see interactive map). 
The readings were recorded at **one-hour** intervals for electricity, chilled water, hot water, steam, irrigation and solar for **2016 and 2017**.
Buildings’ metadata includes year built, size, primary use, site, and source energy use intensity (EUI). Weather data (temperature, pressure, humidity, etc.) 
comes from the National Centers for Environmental Information database.
Our dataset is approximately `2.6 GB` in size, with nearly `53.6` million readings. 

To learn more about the dataset, visit the sites overview page below: '''

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
           

FILTER_STYLE =  {
    'color':'#17B897',
    'font-size':'20px',
    'font-family': 'serif',
    'font-weight': 'bold',
    }

WARNING_STYLE =  {
    'color': '#9F6000',
    # 'background-color': '#FEEFB3',
    'font-size':'20px',
    'font-family': 'serif',
        }
           


tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}