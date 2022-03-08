from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from data import *

# Moved from Data. Since this is a small data load it can be here.
metadata = get_data("/data/metadata/", "metadata.csv", "csv")


def createLayout():
    # Put the header.
    layout = html.Div([Generate_header()])
    # Line break (Space Please)
    layout.children.append(html.Br())

    # To do (put more useful content)
    introRow = html.Div([html.H3('Key Facts:'),
                         Generate_Summary_List()
                         ], className='col-md-2')
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
        html.Div([
            dcc.Graph(id='site_map', style={
                      'height': '55vh'}, figure=plot_map(metadata))
        ], className='col-md-12')
    ], className='row')

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

# TO-DO: move to its own section
# What a mess this thing ain't working!!!!


def Add_Site_Filter() -> dcc.Dropdown:
    sites = list(metadata['site_id'].unique())
    return dcc.Dropdown(sites, sites[0:4], id='Site_Filter', placeholder='Select a site', multi=True)


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
    buildings = get_buidling_by_secondary_usage(metadata, selected_site)
    fig = px.bar(buildings, x='Sites',
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
    # To Do Play with Data here.
    df['Size'] = 50.0

    fig = px.scatter_geo(df, lat='latitude', lon='longitude',
                         locations='site_id', size='Size')

    # fig.add_trace(go.Scattermapbox(
    #         lat=site_lat,
    #         lon=site_lon,
    #         mode='markers',
    #         marker=go.scattermapbox.Marker(
    #             size=17,
    #             color='rgb(255, 0, 0)',
    #             opacity=0.7
    #         ),
    #         text=locations_name,
    #         hoverinfo='text'
    #     ))

    # fig.add_trace(go.Scattermapbox(
    #         lat=site_lat,
    #         lon=site_lon,
    #         mode='markers',
    #         marker=go.scattermapbox.Marker(
    #             size=8,
    #             color='rgb(242, 177, 172)',
    #             opacity=0.7
    #         ),
    #         hoverinfo='none'
    #     ))

    # fig.update_layout(
    #     title='Site location',
    #     autosize=True,
    #     hovermode='closest',
    #     showlegend=False,
    #     mapbox=dict(
    #     pitch=0,
    #     zoom=3,
    #     style='light'
    # )

    # )

    return fig
