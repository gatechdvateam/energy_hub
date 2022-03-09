from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from data import *
import numpy as np

# Moved from Data. Since this is a small data load it can be here.
metadata = get_data("/data/metadata/", "metadata.csv", "csv")


def createLayout():
    # Put the header.
    layout = html.Div([Generate_header()])
    # Line break (Space Please)
    layout.children.append(html.Br())

    # To do (put more useful content)
    introRow = html.Div([html.H2('Data statistics'),
                         compute_stats()
                         ], className='col-md-12')
    layout.children.append(introRow)
    layout.children.append(html.Br())

    # Add Site for once Heavn's Sake
    layout.children.append(
        html.Div([
            Add_Site_Filter(),
            html.Br()
        ], className='col-md-12')
    )

    # Make out Lovely useless Charts.
    chart1 = html.Div([
        html.Br(),
        dcc.Graph(id='building_primary_usage', style={'height': '55vh'})
    ], className='col-md-6')

    chart2 = html.Div([
        html.Br(),
        dcc.Graph(id='building_secondary_usage', style={'height': '55vh'})
    ], className='col-md-6')

    # Add em bad boys.
    chartsRow = html.Div(className='row', children=[chart1, chart2])
    layout.children.append(chartsRow)
    layout.children.append(html.Br())

    # Show Me Some Map or I am shooting someone head spilling their  brain on keyboard.
    MapRow = html.Div([
        html.Br(),
        html.Div([
            dcc.Graph(id='site_map', style={'height': '55vh'}, figure=plot_map(metadata))
        ],  className='row')
    ], className='col-md-12')

    # Just SHOW IT!
    layout.children.append(MapRow)
    layout.children.append(html.Br())

    # Hofff Done!
    return layout


# do we need this function?
# YEAH We need some page intro!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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


def compute_stats():
    n_sites = metadata['site_id'].nunique()
    n_buildings = metadata['building_id'].nunique()
    n_buildings_elec = metadata['building_id'].where(metadata['heating_type'].str.contains("Elect")).nunique()
    n_buildings_gas = metadata['building_id'].where(metadata['heating_type'].str.contains("Gas")).nunique()

    # keep these (will need to use eventualy when we format)
    # columns = ['Total number of sites', 'Total number of buildings']
    # data = np.array([n_sites, n_buildings])

    # table_header = [
    #         html.Thead(html.Tr(html.Tr([html.Th(c) for c in columns])))
    #         ]

    table_header = [
        html.Thead(html.Tr([html.Th("Total sites"), html.Th("Total buildings"),\
                    html.Th("Buildings with electricity as a heating source"),\
                    html.Th("Buildings with gas as a heating source")]))]

    # row1 = html.Tr([html.Td(c) for c in data])

    row1 = html.Tr([html.Td(n_sites), html.Td(n_buildings),\
                 html.Td(n_buildings_elec), html.Td(n_buildings_gas)])

    table_body = [html.Tbody(row1)]

    table = dbc.Table(table_header + table_body,\
                bordered=True,
                dark = True,
                hover=True,
                responsive=True,
                striped=True,)

    return table

# TO-DO: move to its own section
# What a mess this thing ain't working!!!!


def Add_Site_Filter() -> dcc.Dropdown:
    sites = list(metadata['site_id'].unique())
    return dcc.Dropdown(sites, sites[0:3], id='Site_Filter',\
                         placeholder='Select a site', multi=True, clearable=True)


@callback(
    Output('building_primary_usage', 'figure'),
    Input('Site_Filter', 'value'))
def plot_primary_usage(selected_site):
    buildings = get_buidling_by_primary_usage(metadata, selected_site)
    fig = px.bar(buildings, x='Sites',
                 y='Number of Buildings', color='Space Usage')
    fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.2, orientation="h"))

    # TO-DO anchor title to the center
    fig.update_layout(
        title={
            'text': 'sites by primary usage',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})
    return fig


@callback(
    Output('building_secondary_usage', 'figure'),
    Input('Site_Filter', 'value'))
def plot_secondary_usage(selected_site):
    sec_buildings = get_buidling_by_secondary_usage(metadata, selected_site)

    try:
        fig = px.bar(sec_buildings, x='Sites',
                    y='Number of Buildings', color='Space Usage')

    except Exception:
        fig = px.bar(sec_buildings, x='Sites',
                    y='Number of Buildings', color='Space Usage')

    fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.2, orientation="h"))
    fig.update_layout(
        title={
            'text': 'sites by secondary usage',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig



def plot_map(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    

    color = df['site_id'].nunique()

    fig = go.Figure(data=go.Scattergeo(
            lon = df['longitude'],
            lat = df['latitude'],
            text = df['site_id'],
            mode = 'markers',
            # marker_color = df['site_id']
            ))

    fig.update_layout(
        title={
            'text': 'Location of all sites',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'}
        )

    return fig
