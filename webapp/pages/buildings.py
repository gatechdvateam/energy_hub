from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dask.dataframe as dd
from torch import div
from data import *
from content import *


def createLayout():
    title = html.H1('Building Overview & Energy Forecast')
    row = dbc.Row([CreateFilters(),CreateVisuals()])
    return [title,row]

def CreateFilters():
    buildings = CreateSelect(list(metadata['building_id'].unique()),'BuildingFilter','Panther_lodging_Shelia')
    year = CreateSelect([2016,2017],'YearFilter',2016)
    
    
    column=dbc.Col([],md=2,style={'background-color':'#e8e8e8'})
    
    column.children.append(html.H2('Filters'))
    column.children.append(dbc.Label("Select Building:"))
    column.children.append(html.Br())
    column.children.append(dbc.Label(buildings))
    column.children.append(html.Br())
    column.children.append(dbc.Label("Select Year:"))
    column.children.append(html.Br())
    column.children.append(dbc.Label(year))

    return column
    
def CreateVisuals():
    column=dbc.Col([],md=10)
    column.children.append(html.H2('Visuals'))
    return column

def CreateSelect(ItemsList,Name,DefaultValue):
    optionsList = list()
    for item in ItemsList:
        optionsList.append({'label':str(item),'value':str(item)})
    return dbc.Select(id=Name,options=optionsList,value=str(DefaultValue))