# import packages
import calendar
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dask.dataframe as dd
from torch import div
from data import *
from content import *


def createLayout():
    title = html.H2('Building Overview & Energy Forecast', style={"text-align":"center"})
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
    
    
    column=dbc.Col([],md=2,style={'background-color':'#e8e8e8'})
    
    column.children.append(html.H3('Filters'))

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

def CreateSelect(ItemsList,Name,DefaultValue):
    optionsList = list()
    for item in ItemsList:
        optionsList.append({'label':str(item),'value':str(item)})
    return dbc.Select(id=Name,options=optionsList,value=str(DefaultValue),required=True)


@callback(
    Output('electricity', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_electricity(Year,Building):
    data = get_meter_data_for_building('electricity',Building)
    data['Year'] = data.timestamp.dt.year
    data = data[data['Year']==int(Year)]
    data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
    data = data.rename(columns={'timestamp':'Month','electricity':'Electricity Consumption'})
    data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(data, x='Month',
                    y='Electricity Consumption', markers=True,  template="seaborn")
    fig.update_yaxes(ticksuffix =" kW")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    return fig


@callback(
    Output('water', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_water(Year,Building):
    data = get_meter_data_for_building('water',Building)
    data['Year'] = data.timestamp.dt.year
    data = data[data['Year']==int(Year)]
    data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
    data = data.rename(columns={'timestamp':'Month','water':'Water Consumption'})
    data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(data, x='Month',
                    y='Water Consumption', markers=True,  template="seaborn")
    fig.update_yaxes(ticksuffix =" kW")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    return fig


@callback(
    Output('solar', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_solar(Year,Building):
    data = get_meter_data_for_building('solar',Building)
    data['Year'] = data.timestamp.dt.year
    data = data[data['Year']==int(Year)]
    data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
    data = data.rename(columns={'timestamp':'Month','solar':'Solar Consumption'})
    data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(data, x='Month',
                    y='Solar Consumption', markers=True,  template="seaborn")
    fig.update_yaxes(ticksuffix =" kW")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    return fig


@callback(
    Output('gas', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_gas(Year,Building):
    data = get_meter_data_for_building('gas',Building)
    data['Year'] = data.timestamp.dt.year
    data = data[data['Year']==int(Year)]
    data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
    data = data.rename(columns={'timestamp':'Month','gas':'Gas Consumption'})
    data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(data, x='Month',
                    y='Gas Consumption', markers=True,  template="seaborn")
    fig.update_yaxes(ticksuffix =" kW")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    return fig


@callback(
    Output('irrigation', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_irrigation(Year,Building):
    data = get_meter_data_for_building('irrigation',Building)
    data['Year'] = data.timestamp.dt.year
    data = data[data['Year']==int(Year)]
    data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
    data = data.rename(columns={'timestamp':'Month','irrigation':'Irrigation Consumption'})
    data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(data, x='Month',
                    y='Irrigation Consumption', markers=True, template="seaborn")
    fig.update_yaxes(ticksuffix =" kW")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    return fig

@callback(
    Output('steam', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_steam(Year,Building):
    data = get_meter_data_for_building('steam',Building)
    data['Year'] = data.timestamp.dt.year
    data = data[data['Year']==int(Year)]
    data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
    data = data.rename(columns={'timestamp':'Month','steam':'Steam Consumption'})
    data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(data, x='Month',
                    y='Steam Consumption', markers=True,  template="seaborn")
    fig.update_yaxes(ticksuffix =" kW")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    return fig


@callback(
    Output('hotwater', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_hotwater(Year,Building):
    data = get_meter_data_for_building('hotwater',Building)
    data['Year'] = data.timestamp.dt.year
    data = data[data['Year']==int(Year)]
    data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
    data = data.rename(columns={'timestamp':'Month','hotwater':'Hot Water Consumption'})
    data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(data, x='Month',
                    y='Hot Water Consumption', markers=True,  template="seaborn")
    fig.update_yaxes(ticksuffix =" kW")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    return fig


@callback(
    Output('chilledwater', 'figure'),
    Input('YearFilter', 'value'),
    Input('BuildingFilter', 'value'))
def plot_chilledwater(Year,Building):
    data = get_meter_data_for_building('chilledwater',Building)
    data['Year'] = data.timestamp.dt.year
    data = data[data['Year']==int(Year)]
    data = data.groupby(data.timestamp.dt.month).sum().compute().reset_index()
    data = data.rename(columns={'timestamp':'Month','chilledwater':'Chilled Water Consumption'})
    data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
    fig = px.line(data, x='Month',
                    y='Chilled Water Consumption', markers=True, template="seaborn")
    fig.update_yaxes(ticksuffix =" kW")
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
    return fig