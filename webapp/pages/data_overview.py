# import packages
import calendar
import dash
from dash import Dash, dcc, html, Input, Output, callback, no_update, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dask.dataframe as dd
from data import *
from content import *
import plotly.graph_objects as go
from datetime import date
from datetime import datetime
import plotly.figure_factory as ff
import warnings
import numpy as np
import seaborn as sns
warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning) 
# region Layout Functions


def createLayout():
    # title = html.H2('Data Overview: Sites view',
    #                 style={"text-align": "center"})
    row = dbc.Row([CreateFilters(), CreateVisuals()])

     # adding key facts tabs at the end of the page
    key_facts = html.Div(html.Div([
        dbc.Tabs([
            dbc.Tab([
                html.Ul([
                    html.Br(),
                    html.Li('Number of Sites: 19'),
                    html.Li('Number of Buildings: 1636'),
                    html.Li('Number of Meters: 3053'),
                    html.Li('Temporal Coverage: 2016 - 2017'),
                    html.Li([
                        'Data Source: ',
                        html.A('https://github.com/buds-lab/building-data-genome-project-2/wiki',
                                href='https://github.com/buds-lab/building-data-genome-project-2/wiki')
                    ])
                ])

                ], label='Key Facts'),
        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('CSE 6242 Project: Energy Hub Team'),
                html.Li(['GitHub repo: ',
                         html.A('https://github.com/gatechdvateam/project',
                                href='https://github.com/gatechdvateam/project')
                         ])
                ])
            ], label='Project Info')
                ]),

        ], style={'backgroundColor': '#f9f9f9'}))
    return [row, html.Br(), key_facts]


def CreateFilters():

    # make a copy of the data
    building_meta = BuildingMetadata.copy()

    # Create the filters column
    column = dbc.Col([], md=2)

    # select a building
    sites = CreateSelect(list(building_meta['site_id'].unique()), 'SitesFilter',
                             ['Bear', 'Fox','Lamb', 'Moose'], True, True)
    column.children.extend(
        [dbc.Label("Select Sites:"), html.Br(), sites, html.Br()])

    return column


def CreateVisuals():
    """
        This function is responsible for creating the charts area.
    """
    # Create Charts
    primary_usage = dcc.Loading(dcc.Graph(id='primary_usage'), type='default')
    secondary_usage = dcc.Loading(dcc.Graph(id='secondary_usage'), type='default')
    # airtemp = dcc.Loading(dcc.Graph(id='airtemp'), type='default')

    chart1_title = html.H3('Sites overview by primary space usage',
                    style={"text-align": "center"})
    chart2_title = html.H3('Sites overview by secondary space usage',
                    style={"text-align": "center"})
    # chart3_title = html.H3('Weather distribution',
    #                 style={"text-align": "center"})
    column = dbc.Col([html.Br(),chart1_title, html.Br(), primary_usage, html.Br(),
                                chart2_title,html.Br(), secondary_usage], md=10)
    return column

def CreateSelect(ItemsList, Name, DefaultValue=None, Optional=True, Format=False, multiple=True):
    """
    Function to create select lists.
    """
    optionsList = None
    if(Format):
        optionsList = FormatOptions(ItemsList)
    else:
        optionsList = ItemsList
    return dcc.Dropdown(optionsList, DefaultValue, id=Name, clearable=Optional, multi=True)



@callback(
    Output('primary_usage', 'figure'),
    Input('SitesFilter', 'value'))
def plot_primary_usage(selected_site):
 
    primary_usage = get_buidling_by_space_usage(BuildingMetadata.copy(), 'primary_space_usage', selected_site)
   
    fig = px.bar(primary_usage, x='Sites',
                    y='Number of Buildings', color='Space Usage',
                    color_discrete_sequence=ColorPalette, template='simple_white')

    # fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.4, orientation="h"))

    return fig


@callback(
    Output('secondary_usage', 'figure'),
    Input('SitesFilter', 'value'))
def plot_secondary_usage(selected_site):

    secondary_usage = get_buidling_by_space_usage(BuildingMetadata.copy(), 'sub_primary_space_usage', selected_site)

    fig = px.bar(secondary_usage, x='Sites',
                    y='Number of Buildings', color='Space Usage',
                    color_discrete_sequence=ColorPalette, template='simple_white')

    fig.update_layout(legend=dict(y=-0.4, orientation="h"))

    return fig


# @callback(
#     Output('airtemp', 'figure'),
#     Input('SitesFilter', 'value'))
# def plot_weather(selected_site):

#     # site = selected_site[0]
#     # site = selected_site[0]
#     filter_opt = ['air_temperature', 'dew_temperature', 'wind_speed']

#    # get datafarme
#     weather = weatherData[['site_id', 'air_temperature', 'dew_temperature', 'wind_speed']].copy()

#     if (selected_site != None) and (len(selected_site)!=0):
        
        
#         weather = weather.loc[weather['site_id'].isin(selected_site)].reset_index()
    
#     # filter buildings that have primary usage listed
#     # weather = weather[['air_temperature', 'dew_temperature']].notnull()

#     hist_data = [weather[filter_opt[0]].dropna(),
#                 weather[filter_opt[1]].dropna(), weather[filter_opt[2]].dropna()]

#     # colors = ['#2BCDC1', '#F66095']
#     colors = ['#2BCDC1', '#F66095', '#63F50f']

#     # Create distplot with custom bin_size
#     fig = ff.create_distplot(hist_data, group_labels=filter_opt,  bin_size=.5,
#                          colors=colors, curve_type='normal')

#     # fig = px.histogram(weather, x='site_id', y=filter_opt, color='site_id',
#     #                marginal="violin") # or violin, rug)

#     # fig.update_layout(legend=dict(y=-0.4, orientation="h"))

#     return fig



def FormatOptions(Items: list):
    optionsList = list()
    for item in Items:
        label = str(item).replace("_", " ").title()
        optionsList.append({'label': label, 'value': str(item)})
    return optionsList
# endregion
