from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from data import *
from content import *


# Define stats cards
card1 = dbc.CardBody([
        html.H4("Total number of sites"),
        html.P("19", className="card-title")
    ],
    style=STATS_CARD,
    )

card2 = dbc.CardBody([
        html.H4("Total number of buildings for all sites"),
        html.P("1636", className="card-text")
        ],
    style=STATS_CARD,
    )

card3 = dbc.CardBody([
        html.H4("Total number of meters"),
        html.P("3053", className="card-text")
        ],
    style=STATS_CARD,
    )
	
card4 = dbc.CardBody([
        html.H4("Total number of buildings"),
        html.P("700", className="card-title",id="card_text4")
    ],
    style=STATS_CARD,
    )

card5 = dbc.CardBody([
        html.H4("Total number of meters"),
        html.P("1290", className="card-text",id="card_text5")
        ],
    style=STATS_CARD,
    )

card6 = dbc.CardBody([
        html.H4("Total square footage"),
        html.P("400", className="card-text",id="card_text6")
        ],
    style=STATS_CARD,
    )
	
card7 = dbc.CardBody([
        html.H4("The oldest building was built in"),
        html.P("1912", className="card-text",id="card_text7")
        ],
    style=STATS_CARD,
    )
	
	
card8 = dbc.CardBody([
        html.H4("The newest building was built in"),
        html.P("2016", className="card-text",id="card_text8")
        ],
    style=STATS_CARD,
    )
	
card9 = dbc.CardBody([
        html.H4("The max number of floors"),
        html.P("15", className="card-text",id="card_text9")
        ],
    style=STATS_CARD,
    )



def createLayout():
    # Put the header.
    layout = html.Div([generate_header()])
    # Line break (Space Please)
    layout.children.append(html.Br())

    # To do (put more useful content)
    introRow = html.Div([html.H3('Site statistics',  style={'text-align': 'center'}),
                        html.Br(),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Card(card1, color="info", outline=True), md=4),
                                dbc.Col(dbc.Card(card2, color="info", outline=True), md=4),
                                dbc.Col(dbc.Card(card3, color="info", outline=True), md=4),
                            ],
                            style={'marginTop': '10px'}, className='row'
                        ),
                        html.Br(),
                        card_site_selector('card_site'),
                        html.Hr(),
                         ], className='mb-12')



    row_2 = dbc.Row(
        [
            dbc.Col(dbc.Card(card4, color="info", outline=True), md=4),
            dbc.Col(dbc.Card(card5, color="info", outline=True), md=4),
            dbc.Col(dbc.Card(card6, color="info", outline=True), md=4),
        ],
        style={'marginTop': '10px'}, className='row'
    )

    row_3 = dbc.Row(
        [
            dbc.Col(dbc.Card(card7, color="info", outline=True), md=4),
            dbc.Col(dbc.Card(card8, color="info", outline=True), md=4),
            dbc.Col(dbc.Card(card9, color="info", outline=True), md=4),
        ],
        style={'marginTop': '10px'}, className='row'
    )

    cards = html.Div([row_2, row_3])
  
    layout.children.append(introRow)
    layout.children.append(html.Br())
    layout.children.append(cards)
    layout.children.append(html.Br())

    # Section title
    layout.children.append(html.H3('Sites by usage distribution', style={'text-align': 'center'}))
    layout.children.append(html.Hr())

    R2C1 = R2C2 = html.Div(dcc.Markdown(PrimaryUsageMarkDown), className='col-md-6')
    R2C2 = html.Div([
        html.Br(),
        site_id_filter('Prim_Use_Filter'),
        html.Br(),
        dcc.Loading(dcc.Graph(id='building_primary_usage', style={'height': '55vh'}))
    ], className='col-md-6')

    # Make out Lovely useless Charts.
    Row2 = html.Div([R2C1,R2C2], className='row')

    R3C1 = html.Div([
        html.Br(),
        site_id_filter('Sec_Use_Filter'),
        html.Br(),
        dcc.Loading(dcc.Graph(id='building_secondary_usage', style={'height': '55vh'}),type='default')
    ], className='col-md-6')
    R3C2 = R2C2 = html.Div(dcc.Markdown(PrimaryUsageMarkDown), className='col-md-6')

    # Make out Lovely useless Charts.
    Row3 = html.Div([R3C1,R3C2], className='row')
    

    chart2 = html.Div([
        html.Br(),
    ], className='col-md-6')


    # Show Me Some Map or I am shooting someone head spilling their  brain on keyboard.
    MapRow = html.Div(html.Div(
        [
        html.H3('Location of all sites', style={'text-align': 'center'}),
        html.Div(id='MapInput',children=[],style={'display': 'none'}),
        html.Br(),
        dcc.Loading(dcc.Graph(id='site_map', style={'height': '45vh'}))
    ], className='col-md-6'
    ), className='row')

    layout.children.append(Row2)
    layout.children.append(html.Br())
    layout.children.append(Row3)
    layout.children.append(html.Br())
    layout.children.append(MapRow)

    return layout


def generate_header() -> html.Div:
    # Region: Non Changing Elemnts

    header = html.Div([
        html.Div([], className='col-md-6', style={'marginTop': '10px'},)
    ], className='row')
    return header

@callback(
   [
    Output('card_text4','children'),
    Output('card_text5','children'),
    Output('card_text6','children'),
    Output('card_text7','children'),
    Output('card_text8','children'),
    Output('card_text9','children'),
   ],
    Input('card_site','value')
)
def compute_stats(siteID):
    """_summary_

    Returns:
        _type_: _description_
    """
    # select numeric columns
    numeric_columns = metadata.select_dtypes(include=['number']).columns

    # fill -1 to all NaN 
    metadata[numeric_columns] = metadata[numeric_columns].fillna(-1)

    # get total number of sites
    # n_sites = metadata['site_id'].nunique()

    # # get other stats
    # n_buildings_elec = metadata['building_id'].where(metadata['heating_type'].str.contains("Elect")).nunique()
    # n_buildings_gas = metadata['building_id'].where(metadata['heating_type'].str.contains("Gas")).nunique()

    # count of buildings per site
    buildings_grouping = metadata.groupby('site_id',as_index=False)['building_id'].count().reset_index()
    n_buildings = buildings_grouping[buildings_grouping['site_id'] == siteID]['building_id'].values[0]

    # get number of meters per site
    meters = pd.melt(metadata[["site_id","electricity",\
                    "hotwater","chilledwater","steam","water",\
                    "irrigation","gas","solar"]],id_vars = "site_id", var_name="meter")

    n_meters_bysite = meters[meters.value != None].groupby(["site_id","meter"]).count().groupby("site_id").sum().reset_index()
    n_meters = n_meters_bysite[n_meters_bysite['site_id'] == siteID]['value'].values[0]


    # get total square footage per site
    size_per_site_grp = metadata.groupby('site_id',as_index=False)['sq_feet'].sum()
    size_per_site = int(size_per_site_grp[size_per_site_grp['site_id'] == siteID]['sq_feet'].values[0])

    # get oldest buildings year-built
    oldest_building_per_site_grp = metadata[metadata.year_built != None].groupby('site_id',as_index=False)['year_built'].min()
    oldest_building_per_site = int(oldest_building_per_site_grp[oldest_building_per_site_grp['site_id']==siteID]['year_built'].values[0])

    # get newest buildings year-built
    newest_building_per_site_grp = metadata.groupby('site_id',as_index=False)['year_built'].max()
    newest_building_per_site = int(newest_building_per_site_grp[newest_building_per_site_grp['site_id']==siteID]['year_built'].values[0])


    # get max floors per site
    max_num_floors_per_site_grp = metadata[metadata.number_of_floors != None].groupby('site_id',as_index=False)['number_of_floors'].max()
    max_num_floors_per_site = max_num_floors_per_site_grp[max_num_floors_per_site_grp['site_id']==siteID]['number_of_floors'].values[0]


    return n_buildings, n_meters, size_per_site, oldest_building_per_site, newest_building_per_site, max_num_floors_per_site


def card_site_selector(siteID):
    """_summary_

    Returns:
        dcc.Dropdown: _description_
    """
    buildings_grouping = metadata.groupby('site_id',as_index=False)['building_id'].count()
    
    sites = list(buildings_grouping['site_id'])
    return dcc.Dropdown(sites, sites[1], id=siteID, placeholder='select a site')



def site_id_filter(ElementID) -> dcc.Dropdown:
    """_summary_

    Returns:
        dcc.Dropdown: _description_
    """
    # get sites that have at least 10 buildings
    buildings_grouping = metadata.groupby('site_id',as_index=False)['building_id'].count()
    buildings_grouping.sort_values(by=['building_id'],ascending=False)

    buildings_grouping = buildings_grouping[buildings_grouping['building_id'] >= 10]
    
    sites = list(buildings_grouping['site_id'])
    return dcc.Dropdown(sites, sites[0:3], id=ElementID,\
                         placeholder='select a site', multi=True, clearable=True)


@callback(
    Output('building_primary_usage', 'figure'),
    Input('Prim_Use_Filter', 'value'))
def plot_primary_usage(selected_site):
    """_summary_

    Args:
        selected_site (_type_): _description_

    Returns:
        _type_: _description_
    """
    buildings = get_buidling_by_primary_usage(metadata, selected_site)
    # try/except block is needed as workaround. 
    fig = px.bar(buildings, x='Sites',
                    y='Number of Buildings', color='Space Usage',
                    color_discrete_sequence=ColorPalette)

    fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
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
    Output('building_secondary_usage', 'figure'),
    Input('Sec_Use_Filter', 'value'))
def plot_secondary_usage(selected_site):
    """_summary_

    Args:
        selected_site (_type_): _description_

    Returns:
        _type_: _description_
    """
    sec_buildings = get_buidling_by_secondary_usage(metadata, selected_site)

    fig = px.bar(sec_buildings, x='Sites',
                    y='Number of Buildings', color='Space Usage',
                    color_discrete_sequence=ColorPalette)

    fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.4, orientation="h"))
    fig.update_layout(
        title={
            'text': 'sites by secondary usage',
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'})

    return fig


@callback(
    Output('site_map', 'figure'),
    Input('MapInput', 'children'))
def plot_map(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    df = metadata[['site_id','longitude','latitude','building_id']]
    df = df.groupby(['site_id','longitude','latitude'],as_index=False).count()
    df = df.rename(columns={'building_id':'Buildings','site_id' : 'Site'})
    fig = px.scatter_geo(df,lon='longitude', lat='latitude',
            color='Site',
            opacity=0.8,
            size='Buildings',
            size_max=50,
            #Changed Map type
            projection="equirectangular",
            #Changed Palette
            color_discrete_sequence=ColorPalette)

    #Added a zoom projection_scale
    fig.update_layout(
        geo = dict(
            projection_scale=2.7, #Zoom
            center=dict(lat=40.0, lon=-58.0), #Center Point
        ))


    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig