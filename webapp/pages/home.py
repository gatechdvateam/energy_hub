from dash import Dash, dcc, html, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from dataSets import MetaData
# Default Home Page

def createLayout():
    layout = html.Div([Generate_header()])

    layout.children.append(html.Br())

    # col1 = html.Div([html.H3('Key Facts:'),
    #     Generate_Summary_List()
    #                  ], className='col-md-2')

    col2 = html.Div([
        html.H4('Sites by primary usage'),
        Add_Site_Filter(),
        html.Br(),
        dcc.Graph(id='building_primary_usage',style={'height': '55vh'})
    ], className='col-md-6')

    col3 = html.Div([
        html.H4('Sites by secondary space usage'),
        Add_Site_Filter(),
        html.Br(),
        dcc.Graph(id='building_secondary_usage',style={'height': '55vh'})
    ], className='col-md-6')

    dataDiv = html.Div(className='row', children=[col2, col3])

    layout.children.append(dataDiv)

    return layout


def Generate_header() -> html.Div:
    # Region: Non Changing Elemnts
    header = html.Div([
        html.Div([
            html.Img(src='/assets/energy_hub_logo.png',
                 style={
                     'maxHeight': '90px'
                 },
                className='img-fluid float-start')
            # html.H1('Energy Hub'),
            # html.H2('A futuristic energy dashboard'),
        ], className='col-md-6', style={'marginTop': '10px'},)
    ], className='row')
    return header


# this can be replaced by a Dash Table
def Generate_Summary_List() -> html.Ul:
    li1 = html.Li('Number of Buildings: ' +
                  str(MetaData['building_id'].nunique()))
    li2 = html.Li('Number of Sites: ' + str(MetaData['site_id'].nunique()))
    return html.Ul([li1, li2])

# TO-DO: move to its own section
def Add_Site_Filter() -> dcc.Dropdown:
    sites = list(MetaData['site_id'].unique())
    return dcc.Dropdown(sites,sites[0:4],id='Site_Filter',placeholder='Select a site',multi=True)


# all the data aggregation here needs to be elsewhere
@callback(
    Output('building_primary_usage', 'figure'),
    Input('Site_Filter', 'value'))
def building_by_primary_usage(selected_site):
    buildingsbySite = MetaData[['site_id',
                                'building_id', 'primary_space_usage']]
    if selected_site != None and len(selected_site)!=0:
        buildingsbySite = buildingsbySite.loc[buildingsbySite['site_id'].isin(selected_site)]
    buildingsbySite = buildingsbySite[buildingsbySite['primary_space_usage'].notnull(
    )]
    buildingsbySite = buildingsbySite.groupby(
        ['site_id', 'primary_space_usage'], as_index=False).count()
    buildingsbySite = buildingsbySite.rename(columns={'site_id': 'Site Name',
                                                      'building_id': 'Number of Buildings',
                                                      'primary_space_usage': 'Space Usage'})
    buildingsbySite = buildingsbySite.sort_values(by=['Number of Buildings', 'Space Usage'],ascending=False)
    buildingsbySite = buildingsbySite[buildingsbySite['Number of Buildings'] > 15]
    fig = px.bar(buildingsbySite, x='Site Name', y='Number of Buildings', color='Space Usage')
    fig.update_layout(plot_bgcolor='#f9f9f9',paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.2, orientation="h"))
    return fig


@callback(
    Output('building_secondary_usage', 'figure'),
    Input('Site_Filter', 'value'))
def building_by_secondary_usage(selected_site):
    buildingsbySite = MetaData[['site_id',
                                'building_id', 'sub_primary_space_usage']]
    if selected_site != None and len(selected_site)!=0:
        buildingsbySite = buildingsbySite.loc[buildingsbySite['site_id'].isin(selected_site)]
    buildingsbySite = buildingsbySite[buildingsbySite['sub_primary_space_usage'].notnull(
    )]
    buildingsbySite = buildingsbySite.groupby(
        ['site_id', 'sub_primary_space_usage'], as_index=False).count()
    buildingsbySite = buildingsbySite.rename(columns={'site_id': 'Site Name',
                                                      'building_id': 'Number of Buildings',
                                                      'sub_primary_space_usage': 'Space Usage'})
    buildingsbySite = buildingsbySite.sort_values(by=['Number of Buildings', 'Space Usage'],ascending=False)
    buildingsbySite = buildingsbySite[buildingsbySite['Number of Buildings'] > 15]
    fig = px.bar(buildingsbySite, x='Site Name', y='Number of Buildings', color='Space Usage')
    fig.update_layout(plot_bgcolor='#f9f9f9',paper_bgcolor='#f9f9f9')
    fig.update_layout(legend=dict(y=-0.2, orientation="h"))
    return fig