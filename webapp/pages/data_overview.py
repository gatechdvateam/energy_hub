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
from plotly.subplots import make_subplots
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
    return [html.H2('Sites Overview',className='text-center'),html.Br(),key_facts,html.Br(),row, ]


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
    cloud_coverage = dcc.Loading(dcc.Graph(figure=plot_cloud_coverage()), type='default')
    wind_direction = dcc.Loading(dcc.Graph(figure=plot_wind_direction()), type='default')
    weather = dcc.Loading(dcc.Graph(figure=plot_weather()), type='default')
    

    # chart headers
    chart1_title = html.H3('Sites overview by primary space usage',
                    style={"text-align": "center"})
    chart2_title = html.H3('Sites overview by secondary space usage',
                    style={"text-align": "center"})
    chart3_title = html.H3('Cloud coverage',
                    style={"text-align": "center"})
    chart4_title = html.H3('Wind direction',
                    style={"text-align": "center"})

    # Add all to layout
    column = dbc.Col([html.Br(),chart1_title, html.Br(), primary_usage, html.Br(),
                                chart2_title,html.Br(), secondary_usage, html.Br(),
                                chart3_title, cloud_coverage,
                                html.Br(), chart4_title, wind_direction, weather], md=10)
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



def plot_cloud_coverage():

   # get datafarme
    weather = weatherData.copy()

    # Temporal dataframe with cloud cover counts
    temp1 = pd.DataFrame(weather.groupby(["cloud_coverage"]).count().timestamp).rename(columns={"timestamp":"Count"})
    temp_labels1 = temp1["Count"].sort_values().index
    temp_counts1 = temp1["Count"].sort_values()

    fig = px.pie(temp1, values=temp_counts1, names=temp_labels1)

    # fig.update_layout(
    #     title = 'Cloud coverage',
    #     showlegend = False
    # )

    return fig


def plot_wind_direction():

   # get datafarme
    weather = weatherData.copy()

    # Wind direction (radial plot)
    degrees = weather["wind_direction"]
    # print(degrees)
    radians = np.deg2rad(weather["wind_direction"])
    bin_size = 20
    a , b = np.histogram(degrees, bins=np.arange(0, 360+bin_size, bin_size))
    centers = np.deg2rad(np.ediff1d(b)//2 + b[:-1])
    # print(a, b, radians, degrees, centers)

    # Wind direction plot
    fig = go.Figure(go.Barpolar(
                r=a,
                theta=b,
                width=bin_size*centers,
                opacity=0.8
                
            ))


    return fig

def plot_weather():

    # get datafarme
    weather = weatherData.copy()

    # Wind direction (radial plot)
    degrees = weather["wind_direction"]
    bin_size = 20
    a , b = np.histogram(degrees, bins=np.arange(0, 360+bin_size, bin_size))
    centers = np.deg2rad(np.ediff1d(b)//2 + b[:-1])

    fig = make_subplots(rows=1, cols=2, subplot_titles=('Cloud Coverage','Wind Direction'))

    #   # Wind direction plot
    # fig.add_trace(go.Barpolar(
    #             r=a,
    #             theta=b,
    #             width=bin_size*centers,
    #             opacity=0.8
                
    #         )
    #         )

    # Temporal dataframe with cloud cover counts
    temp1 = pd.DataFrame(weather.groupby(["cloud_coverage"]).count().timestamp).rename(columns={"timestamp":"Count"})
    temp_labels1 = temp1["Count"].sort_values().index
    temp_counts1 = temp1["Count"].sort_values()

    # fig.add_trace(px.pie(temp1, values=temp_counts1, names=temp_labels1))

    fig.add_traces(

    [go.Scatter(y=[2, 3, 1]),

     go.Scatterpolar(r=[1, 3, 2], theta=[0, 45, 90]),

                    rows=[1, 1],

                    cols=[1, 2]) 

    return fig


def FormatOptions(Items: list):
    optionsList = list()
    for item in Items:
        label = str(item).replace("_", " ").title()
        optionsList.append({'label': label, 'value': str(item)})
    return optionsList
# endregion
