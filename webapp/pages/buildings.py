# import packages
import calendar
import dash
from dash import Dash, dcc, html, Input, Output, callback, no_update, State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import dask.dataframe as dd
from torch import div
from data import *
from content import *
import plotly.graph_objects as go

#region Layout Functions
def createLayout():
    title = html.H2('Energy consumption: building view',
                    style={"text-align": "center"})
    row = dbc.Row([CreateFilters(), CreateVisuals()])
    return [title, row]


def CreateFilters():
    
    # make a copy of the data
    building_meta = BuildingMetadata.copy()

    # create filter options
    # The below filters affect other filters.
    timezone = CreateSelect(
        list(building_meta['timezone'].unique()), 'TimezoneFilter')
    primary_usage = CreateSelect(
        list(building_meta['primary_space_usage'].unique()), 'UsageFilter')
    building_size = CreateSelect(
        list(building_meta['size'].unique()), 'BuildingSizeFilter')

    # The below filters affect the charts.
    buildings = CreateSelect(list(building_meta['building_id'].unique()), 'BuildingFilter',
                             'Bobcat_education_Alissa', False, True)
    year = CreateSelect([2016, 2017], 'YearFilter', 2017)

    # ,style={'background-color':'#e8e8e8'}
    column = dbc.Col([], md=2)

    column.children.append(html.H3(''))

    # select Timezone/location
    column.children.extend(
        [dbc.Label("Select Time Zone:"), html.Br(), timezone, html.Br()])

    # select primary usage
    column.children.extend(
        [dbc.Label("Select Primary Usage:"), html.Br(), primary_usage, html.Br()])

    # select building size
    # TO-DO (make size buckets)
    column.children.extend(
        [dbc.Label("Select Building Size:"), html.Br(), building_size, html.Br()])

    # select a building
    column.children.extend(
        [dbc.Label("Select Building:"), html.Br(), buildings, html.Br()])

    # select year
    column.children.extend(
        [dbc.Label("Select Year:"), html.Br(), year, html.Br()])

    # Apply Filter
    column.children.extend([html.Button('Apply Filters', id='ApplyFilters', style={"background-color":"yellowgreen","color":"black", "width":"150px"},
                                        n_clicks=0, className="btn btn-primary"), html.Br()])
    return column


def CreateVisuals():
    """
        This function is responsible for creating the charts area.
    """
    # Create Charts
    electricity = dcc.Loading(dcc.Graph(id='electricity'), type='default')
    water = dcc.Loading(dcc.Graph(id='water'), type='default')
    solar = dcc.Loading(dcc.Graph(id='solar'), type='default')
    gas = dcc.Loading(dcc.Graph(id='gas'), type='default')
    steam = dcc.Loading(dcc.Graph(id='steam'), type='default')
    irrigation = dcc.Loading(dcc.Graph(id='irrigation'), type='default')
    hotwater = dcc.Loading(dcc.Graph(id='hotwater'), type='default')
    chilledwater = dcc.Loading(dcc.Graph(id='chilledwater'), type='default')

    column = dbc.Col([electricity, solar, steam, hotwater,
                     water, gas, irrigation, chilledwater], md=10)
    return column
#endregion

#region Callbacks for chart updates
@callback(
    output=[Output('electricity', 'figure'),
            Output('electricity', 'style'), ],
    inputs=[State('YearFilter', 'value'),
            State('BuildingFilter', 'value'),
            Input('ApplyFilters', 'n_clicks')])
def plot_electricity(Year, Building, NC):
    return CreateTimeChart(Year, Building, 'electricity', 'Electricity')


@callback(
    output=[Output('water', 'figure'),
            Output('water', 'style'), ],
    inputs=[State('YearFilter', 'value'),
            State('BuildingFilter', 'value'),
            Input('ApplyFilters', 'n_clicks')])
def plot_water(Year, Building, NC):
    return CreateTimeChart(Year, Building, 'water', 'Water')


@callback(
    output=[Output('gas', 'figure'),
            Output('gas', 'style'), ],
    inputs=[State('YearFilter', 'value'),
            State('BuildingFilter', 'value'),
            Input('ApplyFilters', 'n_clicks')])
def plot_gas(Year, Building, NC):
    return CreateTimeChart(Year, Building, 'gas', 'Gas')


@callback(
    output=[Output('irrigation', 'figure'),
            Output('irrigation', 'style'), ],
    inputs=[State('YearFilter', 'value'),
            State('BuildingFilter', 'value'),
            Input('ApplyFilters', 'n_clicks')])
def plot_irrigation(Year, Building, NC):
    return CreateTimeChart(Year, Building, 'irrigation', 'Irrigation')


@callback(
    output=[Output('solar', 'figure'),
            Output('solar', 'style'), ],
    inputs=[State('YearFilter', 'value'),
            State('BuildingFilter', 'value'),
            Input('ApplyFilters', 'n_clicks')])
def plot_solar(Year, Building, NC):
    return CreateTimeChart(Year, Building, 'solar', 'Solar')


@callback(
    output=[Output('steam', 'figure'),
            Output('steam', 'style'), ],
    inputs=[State('YearFilter', 'value'),
            State('BuildingFilter', 'value'),
            Input('ApplyFilters', 'n_clicks')])
def plot_steam(Year, Building, NC):
    return CreateTimeChart(Year, Building, 'steam', 'Steam')


@callback(
    output=[Output('hotwater', 'figure'),
            Output('hotwater', 'style'), ],
    inputs=[State('YearFilter', 'value'),
            State('BuildingFilter', 'value'),
            Input('ApplyFilters', 'n_clicks')])
def plot_hotwater(Year, Building, NC):
    return CreateTimeChart(Year, Building, 'hotwater', 'Hot Water')


@callback(
    output=[Output('chilledwater', 'figure'),
            Output('chilledwater', 'style'), ],
    inputs=[State('YearFilter', 'value'),
            State('BuildingFilter', 'value'),
            Input('ApplyFilters', 'n_clicks')])
def plot_chilledwater(Year, Building, NC):
    return CreateTimeChart(Year, Building, 'chilledwater', 'Chilled Water')
#endregion

#region Callbacks to update other filters
@callback(
    output=[Output('BuildingFilter', 'options'),
            Output('BuildingFilter', 'value'),
            Output('UsageFilter', 'options'),
            Output('UsageFilter', 'value'),
            Output('BuildingSizeFilter', 'options'),
            Output('BuildingSizeFilter', 'value'),
            Output('TimezoneFilter', 'options'),
            Output('TimezoneFilter', 'value')],
    inputs=[Input('TimezoneFilter', 'value'),
            Input('UsageFilter', 'value'),
            Input('BuildingSizeFilter', 'value')], prevent_initial_call=True)
def FiltersUpdate(TimeZone, Usage, Size):
    ctx = dash.callback_context
    buildings = BuildingMetadata.copy()
    FilterID = ctx.triggered[0]['prop_id'].split('.')[0]

    if (TimeZone != None) and (len(TimeZone) != 0):
        buildings = buildings[buildings['timezone'] == TimeZone]
    if (Usage != None) and (len(Usage) != 0):
        buildings = buildings[buildings['primary_space_usage'] == Usage]
    if (Size != None) and (len(Size) != 0):
        buildings = buildings[buildings['size'] == Size]

    outputs = list()
    BuildingOptions = list(buildings['building_id'].unique())
    Buildingval = BuildingOptions[0]
    outputs.extend([BuildingOptions, Buildingval])

    if FilterID != 'UsageFilter':
        UsageOptions = list(buildings['primary_space_usage'].unique())
        outputs.extend([UsageOptions, no_update])
    else:
        outputs.extend([no_update, no_update])

    if FilterID != 'BuildingSizeFilter':
        SizeOptions = list(buildings['size'].unique())
        outputs.extend([SizeOptions, no_update])
    else:
        outputs.extend([no_update, no_update])

    if FilterID != 'TimezoneFilter':
        TimezoneOptions = list(buildings['timezone'].unique())
        outputs.extend([TimezoneOptions, no_update])
    else:
        outputs.extend([no_update, no_update])

    return outputs
#endregion

#region support functions to create charts and filters
def CreateSelect(ItemsList, Name, DefaultValue=None, Optional=True, Format=False):
    """
    Function to create select lists.
    """
    optionsList = None
    if(Format):
        optionsList = FormatOptions(ItemsList)
    else:
        optionsList = ItemsList
    return dcc.Dropdown(optionsList, DefaultValue, id=Name, clearable=Optional)


def CreateTimeChart(Year: str, BuildingName: str, MeterName: str, ValuesColumnName: str):
    """
    Function that checks if the meter data is available for a given building and
    creates a chart for that.
    """
    building_data = BuildingMetadata[BuildingMetadata['building_id']
                                     == BuildingName].iloc[0]
    if str(building_data[MeterName]) == 'True':
        data = get_meter_data_for_building(MeterName, BuildingName)
        data['Year'] = data.timestamp.dt.year
        data = data[data['Year'] == int(Year)]
        data = data.groupby(
            data.timestamp.dt.month).sum().compute().reset_index()
        data = data.rename(columns={'timestamp': 'Month', MeterName: (
            ValuesColumnName + ' Consumption')})
        data['Month'] = data['Month'].apply(lambda x: calendar.month_abbr[x])
        fig = px.line(data, x='Month',
                      y=ValuesColumnName + ' Consumption', markers=True,  template="plotly")
        fig.update_yaxes(ticksuffix=" kW")
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black')
        return [fig, {'display': 'block'}]
    else:
        return [no_update, {'display': 'none'}]

#endregion

#region Supporting Functions
def FormatOptions(Items: list):
    optionsList = list()
    for item in Items:
        label = str(item).replace("_", " ").title()
        optionsList.append({'label': label, 'value': str(item)})
    return optionsList

#endregion
