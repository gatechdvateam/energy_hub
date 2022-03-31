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
# region Layout Functions


def createLayout():
    title = html.H2('Data Overview: Sites view',
                    style={"text-align": "center"})
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
    return [title, html.Br(), row, html.Br(), key_facts]


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
    column = dbc.Col([primary_usage, html.Br(), secondary_usage], md=10)
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

    fig.update_layout(
        title={
            'text': 'sites by primary usage',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig


@callback(
    Output('secondary_usage', 'figure'),
    Input('SitesFilter', 'value'))
def plot_secondary_usage(selected_site):

    secondary_usage = get_buidling_by_space_usage(BuildingMetadata.copy(), 'sub_primary_space_usage', selected_site)

    fig = px.bar(secondary_usage, x='Sites',
                    y='Number of Buildings', color='Space Usage',
                    color_discrete_sequence=ColorPalette, template='simple_white')

    # fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.4, orientation="h"))
    fig.update_layout(
        title={
            'text': 'sites by secondary usage',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig


def FormatOptions(Items: list):
    optionsList = list()
    for item in Items:
        label = str(item).replace("_", " ").title()
        optionsList.append({'label': label, 'value': str(item)})
    return optionsList
# endregion
