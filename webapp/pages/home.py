from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from data import *


def createLayout():
    layout = html.Div([Generate_header()])

    # layout = html.Div()

    layout.children.append(html.Br())

    # col1 = html.Div([html.H3('Key Facts:'),
    #     Generate_Summary_List()
    #                  ], className='col-md-2')

    col2 = html.Div([
        Add_Site_Filter(),
        html.Br(),
        dcc.Graph(id='building_primary_usage',style={'height': '55vh'})
    ], className='col-md-6')

    col3 = html.Div([
        Add_Site_Filter(),
        html.Br(),
        dcc.Graph(id='building_secondary_usage',style={'height': '55vh'})
    ], className='col-md-6')

    # col4 = html.Div([
    #     dcc.Graph(id='site_map',style={'height': '55vh'}, figure=plot_map(metadata)),
    # ], className='col-md-12')

    # site_map = html.Div(className='row', children=col4)
    dataDiv = html.Div(className='row', children=[col2, col3])


    # layout.children.append(site_map)
    layout.children.append(dataDiv)

    return layout


# do we need this function?
def Generate_header() -> html.Div:
    # Region: Non Changing Elemnts

    header = html.Div([
        html.Div([], className='col-md-6', style={'marginTop': '10px'},)
    ], className='row')
    return header


# this can be replaced by a Dash Table
def Generate_Summary_List() -> html.Ul:
    li1 = html.Li('Number of Buildings: ' +
                  str(metadata['building_id'].nunique()))
    li2 = html.Li('Number of Sites: ' + str(metadata['site_id'].nunique()))
    return html.Ul([li1, li2])

# TO-DO: move to its own section
def Add_Site_Filter() -> dcc.Dropdown:
    sites = list(metadata['site_id'].unique())
    return dcc.Dropdown(sites,sites[0:4],id='Site_Filter',placeholder='Select a site',multi=True)



@callback(
    Output('building_primary_usage', 'figure'),
    Input('Site_Filter', 'value'))
def plot_primary_usage(selected_site):
    buildings = get_buidling_by_primary_usage(metadata, selected_site)
    fig = px.bar(buildings, x='Sites', y='Number of Buildings', color='Space Usage')
    fig.update_layout(plot_bgcolor='#f9f9f9',paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.2, orientation="h"))

    # TO-DO anchor title to the center
    fig.update_layout(
        title={
        'text': 'sites by primary usage',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    return fig


@callback(
    Output('building_secondary_usage', 'figure'),
    Input('Site_Filter', 'value'))
def plot_secondary_usage(selected_site):
    buildings = get_buidling_by_secondary_usage(metadata, selected_site)
    fig = px.bar(buildings, x='Sites', y='Number of Buildings', color='Space Usage')
    fig.update_layout(plot_bgcolor='#f9f9f9',paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.2, orientation="h"))
    fig.update_layout(
        title={
        'text': 'sites by secondary usage',
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    return fig


