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
from plotly.offline import plot
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
        dbc.Tabs(children=[
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

                ], label='Key Facts', style=tab_style, active_label_style=tab_selected_style),

        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('Electricity'),
                html.Li('Gas'),
                html.Li('Steam'),
                html.Li('Chilled water'),
                html.Li('Hot water'),
                html.Li('Solar'),
                html.Li('Irrigation'),

                ])
            ], label='Available Meters', style=tab_style, active_label_style=tab_selected_style),

        dbc.Tab([
            html.Ul([
                html.Br(),
                html.Li('CSE 6242 Project: Energy Hub Team'),
                html.Li(['GitHub repo: ',
                         html.A('https://github.com/gatechdvateam/project',
                                href='https://github.com/gatechdvateam/project')
                         ])
                ])
            ], label='Project Info', style=tab_style, active_label_style=tab_selected_style),
                ],  style=tabs_styles),


        ], ))
    return [html.Br(),html.H2('Sites Overview',className='text-center'),html.Br(),key_facts,html.Br(),row, ]

# style={'backgroundColor': '#f9f9f9'}
def CreateFilters():

    # make a copy of the data
    building_meta = BuildingMetadata.copy()

    # Create the filters column
    column = dbc.Col([], md=2)

    # select a building
    sites = CreateSelect(list(building_meta['site_id'].unique()), 'SitesFilter',
                             ['Rat', 'Bull','Panther', 'Eagle'], True, True)
    column.children.extend(
        [dbc.Label("Sites:", style=FILTER_STYLE), html.Br(), sites, html.Br()])

    return column


def CreateVisuals():
    """
        This function is responsible for creating the charts area.
    """
    # Create Charts
    primary_usage = dcc.Loading(dcc.Graph(id='primary_usage'), type='default')
    secondary_usage = dcc.Loading(dcc.Graph(id='secondary_usage'), type='default')
    weather = dcc.Loading(dcc.Graph(figure=plot_weather()), type='default')
    temp = dcc.Loading(dcc.Graph(figure=plot_temp()), type='default')
    wind_dir = dcc.Loading(dcc.Graph(figure=plot_wind_direction()), type='default')
    cloud_cov = dcc.Loading(dcc.Graph(figure=plot_cloud_cov()), type='default')
    

    # chart headers
    chart1_title = html.H3('Sites overview by primary space usage',
                    style={"text-align": "center"})
    chart2_title = html.H3('Sites overview by secondary space usage',
                    style={"text-align": "center"})
    chart3_title = html.H3('Weather across all sites in 2016-2017',
                    style={"text-align": "center"})

    # Add all to layout
    column = dbc.Col([html.Br(),chart1_title, html.Br(), primary_usage, html.Br(),
                                chart2_title,html.Br(), secondary_usage, html.Br(),
                                chart3_title, html.Br(), temp, html.Br(),
                                cloud_cov, html.Br(), wind_dir], md=10)

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


def plot_weather():

    # get datafarme
    weather = weatherData.copy()

    # Wind direction (radial plot)
    degrees = weather["wind_direction"]
    bin_size = 20
    a , b = np.histogram(degrees, bins=np.arange(0, 360+bin_size, bin_size))
    centers = np.deg2rad(np.ediff1d(b)//2 + b[:-1])

    # Temporal dataframe with cloud cover counts
    cloud_cov = pd.DataFrame(weather.groupby(["cloud_coverage"]).count().timestamp).rename(columns={"timestamp":"Count"})
    labels_temp = cloud_cov["Count"].sort_values().index
    counts = cloud_cov["Count"].sort_values()
    labels = [str(int(label)) + " Oktas" for label in labels_temp]
    labels_more_info = []
    for label in labels:
        if label == '0 Oktas':
            labels_more_info.append(label + " (Sky completely clear)")
        elif label == '4 Oktas':
            labels_more_info.append(label + " (Sky half cloudy)")
        elif label == '8 Oktas':
            labels_more_info.append(label + " (Sky completely cloudy)")
        elif label == '9 Oktas':
            labels_more_info.append(label + " (Sky obstructed from view)")
        else:
            labels_more_info.append(label)

    
    sorted_labels = sorted(labels_more_info, key = lambda x: int(x[0]))[::-1]
    # creating subplots
    fig = make_subplots(rows=2, cols=1, vertical_spacing=1.0,
                            subplot_titles=('Cloud Coverage measured in Oktas', "Wind Direction"), 
                            specs=[[{"type": "pie"}], [{"type": "barpolar"}]])


    fig.add_trace(go.Pie(
                values=counts,
                labels=sorted_labels,
                domain=dict(x=[0, 1.0]),
                name="Cloud coverage",
                hoverinfo="label+percent+name",
                legendgroup = '1',
            ), 
        row=1, col=1)


    fig.add_trace(go.Barpolar(
                 r=a,
                theta=b,
                width=bin_size,
                opacity=0.5,
                name="Wind Direction",
                hoverinfo="r+theta+name",
                legendgroup = '2',
            ),
        row=2, col=1)
        
   
    fig.update_layout(
            legend_tracegroupgap = 40,
            plot_bgcolor="white",
            width=900,
            height=900,
            legend=dict(
                font=dict(family="sans-serif", size=12),
                # bgcolor="white",
                # bordercolor="black",
                # borderwidth=2,
                ),
            )

    fig.update_layout(legend=dict(
                    orientation="v",
                    yanchor="bottom",
                    y=0.99,
                    xanchor="right",
                    x=0.01
        ))

    return fig

def plot_cloud_cov():

    # get datafarme
    weather = weatherData.copy()

    # Temporal dataframe with cloud cover counts
    cloud_cov = pd.DataFrame(weather.groupby(["cloud_coverage"]).count().timestamp).rename(columns={"timestamp":"Count"})
    labels_temp = cloud_cov["Count"].sort_values().index
    counts = cloud_cov["Count"].sort_values()
    labels = [str(int(label)) + " Oktas" for label in labels_temp]
    labels_more_info = []
    for label in labels:
        if label == '0 Oktas':
            labels_more_info.append(label + " (Sky completely clear)")
        elif label == '4 Oktas':
            labels_more_info.append(label + " (Sky half cloudy)")
        elif label == '8 Oktas':
            labels_more_info.append(label + " (Sky completely cloudy)")
        elif label == '9 Oktas':
            labels_more_info.append(label + " (Sky obstructed from view)")
        else:
            labels_more_info.append(label)

    
    sorted_labels = sorted(labels_more_info, key = lambda x: int(x[0]))[::-1]

    fig = go.Figure()
    fig.add_trace(go.Pie(
                values=counts,
                labels=sorted_labels,
                domain=dict(x=[0, 1.0]),
                name="Cloud coverage",
                hoverinfo="label+percent+name",
                
            ))
        
   
    fig['data'][0]['showlegend'] = True

 
    fig.update_layout(
        legend=dict(
            title_font_family="Calibri",
            font=dict(
                family="Calibri",
                size=16,
                color="black"
            ),
            bgcolor="white",
            bordercolor="lightBlue",
            borderwidth=1
        )
    )
    fig.update_layout(height=600)
    # fig.update_layout(legend=dict(
    #         orientation="h",
    #         yanchor="bottom",
    #         y=-.7,
    #         xanchor="right",
    #         x=1
    #     ), legend_title='Cloud Coverage')

    #Don't do this. Prevents Mobile Flex.
    # fig.update_layout(
    #     autosize=False,
    #     width=1500,
    #     height=600,
    #     margin=dict(
    #         l=50,
    #         r=50,
    #         b=100,
    #         t=100,
    #         pad=4
    #     ),
    #     # paper_bgcolor="LightSteelBlue",
    # )

    # fig.update_layout(title_text='Cloud Coverage across all sites', title_x=0.5)


    return fig

def plot_wind_direction():

    # get datafarme
    weather = weatherData.copy()

    # Wind direction (radial plot)
    degrees = weather["wind_direction"]
    bin_size = 20
    a , b = np.histogram(degrees, bins=np.arange(0, 360+bin_size, bin_size))
    centers = np.deg2rad(np.ediff1d(b)//2 + b[:-1])

    fig = go.Figure()
    fig.add_trace(go.Barpolar(
                r=a,
                theta=b,
                width=bin_size,
                opacity=0.5,
                name="Wind Direction",
                hoverinfo="r+theta+name",
            ))
        
    
    fig['data'][0]['showlegend'] = True

    fig.update_layout(
        legend=dict(
            title_font_family="Calibri",
            font=dict(
                family="Calibri",
                size=16,
                color="black"
            ),
            bgcolor="white",
            bordercolor="lightBlue",
            borderwidth=1
        )
    )
    fig.update_layout(height=600)
    #Don't do this. Prevents Mobile Flex.
    # fig.update_layout(
    #         autosize=False,
    #         width=1300,
    #         height=600,
    #         margin=dict(
    #             l=50,
    #             r=50,
    #             b=100,
    #             t=100,
    #             pad=4
    #         ),
    #         # paper_bgcolor="LightSteelBlue",
    #     )

    fig.update_layout(legend=dict(
            orientation="v",
            yanchor="bottom",
            y=0.02,
            xanchor="right",
            x=1
        ))
    # fig.update_layout(title_text='Wind direction across all sites', title_x=0.5)


    return fig


def plot_temp():

    # get datafarme
    weather = weatherData.copy()

    # Group data together
    x0 = weather["air_temperature"].dropna()
    x1 = weather["dew_temperature"].dropna()
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=x0,
        histnorm='probability',
        name='Air Temperature (ºC)', # name used in legend and hover labels
        nbinsx= 100,
        marker_color='#EB89B5',
        opacity=0.75
    ))
    fig.add_trace(go.Histogram(
        x=x1,
        histnorm='probability',
        name='Dew Temperature (ºC)',
        nbinsx= 150,
        marker_color='#330C73',
        opacity=0.8
    ))

    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title_text='Temprature (ºC)', # xaxis label
        yaxis_title_text='Count', # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )

    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return fig


def FormatOptions(Items: list):
    optionsList = list()
    for item in Items:
        label = str(item).replace("_", " ").title()
        optionsList.append({'label': label, 'value': str(item)})
    return optionsList
# endregion
