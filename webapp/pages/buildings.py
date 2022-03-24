# import packages
import calendar
from dash import Dash, dcc, html, Input, Output, callback, no_update
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dask.dataframe as dd
from torch import div
from data import *
from content import *
import plotly.graph_objects as go

def createLayout():
    title = html.H2('Energy consumption: building view', style={"text-align":"center"})
    col1,col2 = CreateVisuals()
    row = dbc.Row([CreateFilters(),col1,col2])
    return [title,row]

def CreateFilters():
    # make a copy of the data
    building_meta = BuildingMetadata.copy()
    # get data where sq feet is not null
    building_meta = building_meta.loc[building_meta['sq_feet'].notnull()]

    # create a bucket for building size
    building_meta['size'] = pd.cut(building_meta['sq_feet'], 3, labels=['Small', 'Medium', 'Large'])

    # create filter options
    timezone = CreateSelect(list(building_meta['timezone'].unique()),'LocationFilter','US.Eastern')
    primary_usage= CreateSelect(list(building_meta['primary_space_usage'].unique()),'UsageFilter','Office')
    building_size = CreateSelect(list(building_meta['size'].unique()),'BuildingSizeFilter','Small')
    buildings = CreateSelect(list(building_meta['building_id'].unique()),'BuildingFilter','Bobcat_education_Alissa')
    year = CreateSelect([2016,2017],'YearFilter',2017)
    
    # ,style={'background-color':'#e8e8e8'}
    column=dbc.Col([],md=2)
    
    column.children.append(html.H3(''))

    # select Timezone/location
    column.children.extend([dbc.Label("Select Time Zone:"),html.Br(),dbc.Label(timezone),html.Br()])

    # select primary usage
    column.children.extend([dbc.Label("Select Primary Usage:"),html.Br(),dbc.Label(primary_usage),html.Br()])

    # select building size
    # TO-DO (make size buckets)
    column.children.extend([dbc.Label("Select Building Size:"),html.Br(),dbc.Label(building_size),html.Br()])

    # select a building
    column.children.extend([dbc.Label("Select Building:"),html.Br(),dbc.Label(buildings),html.Br()])

    # select year
    column.children.extend([dbc.Label("Select Year:"),html.Br(),dbc.Label(year),html.Br()])

    return column
    
def CreateVisuals():

    #Create Charts
    electricity = dcc.Loading(dcc.Graph(id='electricity'),type='default')
    water = dcc.Loading(dcc.Graph(id='water'),type='default')
    solar = dcc.Loading(dcc.Graph(id='solar'),type='default')
    gas = dcc.Loading(dcc.Graph(id='gas'),type='default')
    steam = dcc.Loading(dcc.Graph(id='steam'),type='default')
    irrigation = dcc.Loading(dcc.Graph(id='irrigation'),type='default')
    hotwater = dcc.Loading(dcc.Graph(id='hotwater'),type='default')
    chilledwater = dcc.Loading(dcc.Graph(id='chilledwater'),type='default')
    #Create 2 columns.
    #We will split our visual into sets of 2 columns.

    left = dbc.Col([electricity, solar, steam, hotwater],md=5)
    right = dbc.Col([water, gas, irrigation, chilledwater],md=5)


    return [left, right]

#Output order is important.
@callback(
    Output('electricity', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_electricity(Year,Building):
    return CreateTimeChart(Year,Building,'electricity','Electricity')

@callback(
    Output('water', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_water(Year,Building):
    return CreateTimeChart(Year,Building,'water','Water')

@callback(
    Output('gas', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_gas(Year,Building):
    return CreateTimeChart(Year,Building,'gas','Gas')

@callback(
    Output('irrigation', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_irrigation(Year,Building):
    return CreateTimeChart(Year,Building,'irrigation','Irrigation')

@callback(
    Output('solar', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_solar(Year,Building):
    return CreateTimeChart(Year,Building,'solar','Solar')

@callback(
    Output('steam', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_steam(Year,Building):
    return CreateTimeChart(Year,Building,'steam','Steam')

@callback(
    Output('hotwater', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_hotwater(Year,Building):
    return CreateTimeChart(Year,Building,'hotwater','Hot Water')

@callback(
    Output('chilledwater', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_chilledwater(Year,Building):
    return CreateTimeChart(Year,Building,'chilledwater','Chilled Water')

def CreateSelect(ItemsList,Name,DefaultValue):
    """
    Function to create select lists.
    """
    optionsList = list()
    for item in ItemsList:
        optionsList.append({'label':str(item),'value':str(item)})
    return dbc.Select(id=Name,options=optionsList,value=str(DefaultValue),required=True)

def CreateTimeChart(Year:str, BuildingName:str, MeterName:str, ValuesColumnName:str):
    """
    Function that checks if the meter data is available for a given building and
    creates a chart for that.
    """
    building_data = BuildingMetadata[BuildingMetadata['building_id']==BuildingName].iloc[0]
    if str(building_data[MeterName])=='True':
        data = get_meter_data_for_building(MeterName,BuildingName)
        data['Year'] = data.timestamp.dt.year
        data = data[data['Year']==int(Year)]
        data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
        data = data.rename(columns={'timestamp':'Month', MeterName: (ValuesColumnName + ' Consumption')})
        data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
        fig = px.line(data, x='Month',
                        y=ValuesColumnName + ' Consumption', markers=True,  template="plotly")
        fig.update_yaxes(ticksuffix =" kW")
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
        return fig
    else:
        fig = go.Figure()
        fig.update_layout(
            xaxis =  { "visible": False },yaxis = { "visible": False },
            annotations = [{ "text": "No data available for: "+ValuesColumnName,
                    "xref": "paper","yref": "paper","showarrow": False,
                    "font": {"size": 28}}])
        return fig