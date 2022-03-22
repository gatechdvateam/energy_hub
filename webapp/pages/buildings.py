from distutils.command.build import build
from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dask.dataframe as dd
from torch import div
from data import *
from content import *


def createLayout():
    title = html.H2('Building Overview & Energy Forecast')
    row = dbc.Row([CreateFilters(),CreateVisuals()])
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
    buildings = CreateSelect(list(building_meta['building_id'].unique()),'BuildingFilter','Panther_lodging_Shelia')
    year = CreateSelect([2016,2017],'YearFilter',2016)
    
    
    column=dbc.Col([],md=2,style={'background-color':'#e8e8e8'})
    
    column.children.append(html.H3('Filters'))

    # select Timezone/location
    column.children.append(dbc.Label("Select Time Zone:"))
    column.children.append(html.Br())
    column.children.append(dbc.Label(timezone))
    column.children.append(html.Br())

    # select primary usage
    column.children.append(dbc.Label("Select Primary Usage:"))
    column.children.append(html.Br())
    column.children.append(dbc.Label(primary_usage))
    column.children.append(html.Br())

    # select building size
    # TO-DO (make size buckets)
    column.children.append(dbc.Label("Select Building Size:"))
    column.children.append(html.Br())
    column.children.append(dbc.Label(building_size))
    column.children.append(html.Br())

    # select a building
    column.children.append(dbc.Label("Select Building:"))
    column.children.append(html.Br())
    column.children.append(dbc.Label(buildings))
    column.children.append(html.Br())

    # select year
    column.children.append(dbc.Label("Select Year:"))
    column.children.append(html.Br())
    column.children.append(dbc.Label(year))

    return column
    
def CreateVisuals():
    column=dbc.Col([],md=10)
    column.children.append(html.H3('Visuals'))
    return column

def CreateSelect(ItemsList,Name,DefaultValue):
    optionsList = list()
    for item in ItemsList:
        optionsList.append({'label':str(item),'value':str(item)})
    return dbc.Select(id=Name,options=optionsList,value=str(DefaultValue))