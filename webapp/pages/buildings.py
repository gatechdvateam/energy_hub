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
    title = html.H2('Building Energy Profile',
                    style={"text-align": "center"})
    row = dbc.Row([CreateFilters(), CreateVisuals()])
    return [title, row]


def CreateFilters():

    # make a copy of the data
    building_meta = BuildingMetadata.copy()

    # Create the filters column
    column = dbc.Col([], md=2)

    # select Timezone/location
    timezone = CreateSelect(
        list(building_meta['timezone'].unique()), 'TimezoneFilter')
    column.children.extend(
        [dbc.Label("Select Time Zone:"), html.Br(), timezone, html.Br()])

    # select primary usage
    primary_usage = CreateSelect(
        list(building_meta['primary_space_usage'].unique()), 'UsageFilter')
    column.children.extend(
        [dbc.Label("Select Primary Usage:"), html.Br(), primary_usage, html.Br()])

    # select building size
    # TO-DO (make size buckets)
    building_size = CreateSelect(
        list(building_meta['size'].unique()), 'BuildingSizeFilter')
    column.children.extend(
        [dbc.Label("Select Building Size:"), html.Br(), building_size, html.Br()])

    # select a building
    buildings = CreateSelect(list(building_meta['building_id'].unique()), 'BuildingFilter',
                             'Hog_parking_Shannon', False, True)
    column.children.extend(
        [dbc.Label("Select Building:"), html.Br(), buildings, html.Br()])

    # select Aggregation Level
    level = CreateSelect(['Month', 'Quarter', 'Week', 'None'],
                         'BP_AggLevelFilter', 'None')
    column.children.extend(
        [dbc.Label("Select Aggregation Level:"), html.Br(), level, html.Br()])

    # select Aggregation Type
    ty_pe = CreateSelect(['Sum', 'Avg', 'Max', 'Min'],
                         'BP_AggTypeFilter', 'Sum')
    column.children.extend(
        [dbc.Label("Select Aggregation Type: *"), html.Br(), ty_pe, html.Br()])

    # select Dates
    dates = dcc.DatePickerRange(
        id='DateFilter',
        min_date_allowed=date(2016, 1, 1),
        max_date_allowed=date(2017, 12, 31),
        start_date=date(2017, 1, 1),
        end_date=date(2017, 1, 2)
    )
    column.children.extend(
        [dbc.Label("Select Start & End Dates:"), html.Br(), dates, html.Br(), html.Br()])

    # Apply Filter
    column.children.extend([html.Button('Apply Filters', id='ApplyFilters', style={"background-color": "yellowgreen", "color": "black", "width": "150px"},
                                        n_clicks=0, className="btn btn-primary"), html.Br()])
    column.children.append(html.P(children=[
        '*Not supported for aggregation level None.'
        ],className='text-warning'))
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

    column = dbc.Col([electricity, html.Br(), solar, html.Br(),
                      steam, html.Br(), hotwater, html.Br(),
                      water, html.Br(), gas, html.Br(),
                      irrigation, html.Br(), chilledwater], md=10)
    return column
# endregion


# region Callbacks for chart updates

# Define the list of inputs that affects the chart re render one time here rather than repeat.
filterInputList = {"Values": {
    "Building": State('BuildingFilter', 'value'),
    "StartDate": State('DateFilter', 'start_date'),
    "EndDate": State('DateFilter', 'end_date'),
    "AggLevel": State('BP_AggLevelFilter', 'value'),
    "AggType": State('BP_AggTypeFilter', 'value'),
    "NC": Input('ApplyFilters', 'n_clicks')
}}


@callback(
    output=[Output('electricity', 'figure'),
            Output('electricity', 'style'), ],
    inputs=filterInputList)
def plot_electricity(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building"], 'electricity', 'Electricity',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'])


@callback(
    output=[Output('water', 'figure'),
            Output('water', 'style'), ],
    inputs=filterInputList)
def plot_water(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building"], 'water', 'Water',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'],MeasurementUnit='L')


@callback(
    output=[Output('gas', 'figure'),
            Output('gas', 'style'), ],
    inputs=filterInputList)
def plot_gas(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building"], 'gas', 'Gas',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'],MeasurementUnit='L')


@callback(
    output=[Output('irrigation', 'figure'),
            Output('irrigation', 'style'), ],
    inputs=filterInputList)
def plot_irrigation(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building"], 'irrigation', 'Irrigation',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'],MeasurementUnit='L')


@callback(
    output=[Output('solar', 'figure'),
            Output('solar', 'style'), ],
    inputs=filterInputList)
def plot_solar(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building"], 'solar', 'Solar',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'])


@callback(
    output=[Output('steam', 'figure'),
            Output('steam', 'style'), ],
    inputs=filterInputList)
def plot_steam(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building"], 'steam', 'Steam',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'],MeasurementUnit='L')


@callback(
    output=[Output('hotwater', 'figure'),
            Output('hotwater', 'style'), ],
    inputs=filterInputList)
def plot_hotwater(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building"], 'hotwater', 'Hot Water',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'],MeasurementUnit='L')


@callback(
    output=[Output('chilledwater', 'figure'),
            Output('chilledwater', 'style'), ],
    inputs=filterInputList)
def plot_chilledwater(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building"], 'chilledwater', 'Chilled Water',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'],MeasurementUnit='L')
# endregion


# region Callbacks to update other filters

# Define Outputs here
filtersUpdateOutputs = [Output('BuildingFilter', 'options'),
                        Output('BuildingFilter', 'value'),
                        Output('UsageFilter', 'options'),
                        Output('UsageFilter', 'value'),
                        Output('BuildingSizeFilter', 'options'),
                        Output('BuildingSizeFilter', 'value'),
                        Output('TimezoneFilter', 'options'),
                        Output('TimezoneFilter', 'value')]
# Define Inputs here
filtersUpdateInputs = [Input('TimezoneFilter', 'value'),
                       Input('UsageFilter', 'value'),
                       Input('BuildingSizeFilter', 'value')]


@callback(
    output=filtersUpdateOutputs,
    inputs=filtersUpdateInputs, prevent_initial_call=True)
def FiltersUpdate(TimeZone, Usage, Size):
    # Get the current context to identify which of the inputs was updated
    ctx = dash.callback_context
    # Get the name of the item that was updated.
    FilterID = ctx.triggered[0]['prop_id'].split('.')[0]
    # Get the list of buildings
    buildings = BuildingMetadata.copy()

    # Now we filter the buildings list based on the selected options.
    if (TimeZone != None) and (len(TimeZone) != 0):
        buildings = buildings[buildings['timezone'] == TimeZone]
    if (Usage != None) and (len(Usage) != 0):
        buildings = buildings[buildings['primary_space_usage'] == Usage]
    if (Size != None) and (len(Size) != 0):
        buildings = buildings[buildings['size'] == Size]

    # Define an empty list that will house all outputs.
    outputs = list()

    # Get available buildings that match the criteria
    BuildingOptions = list(buildings['building_id'].unique())
    # Get the first building.
    Buildingval = BuildingOptions[0]
    # Format the names of the buildings
    BuildingOptions = FormatOptions(BuildingOptions)
    # Add to list of inputs.
    outputs.extend([BuildingOptions, Buildingval])

    # if the filter was not updated, i.e. the user didn't play with this value
    # We get the list of available values for all filters below.
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


filterInputList = {"Values": {
    "Building": State('BuildingFilter', 'value'),
    "StartDate": State('DateFilter', 'start_date'),
    "EndDate": State('DateFilter', 'end_date'),
    "AggLevel": State('BP_AggLevelFilter', 'value'),
    "AggType": State('BP_AggTypeFilter', 'value'),
    "NC": Input('ApplyFilters', 'n_clicks')
}}

# endregion

# region support functions to create charts and filters
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


def CreateTimeChart(Start: str, End: str, BuildingName: str, MeterName: str,
                    ValuesColumnName: str, MeasurementUnit: str = " kW", AggLevel: str = 'Month', aggFunction='Sum'):
    """
    Function that checks if the meter data is available for a given building and
    creates a chart for that.
    """

    # Load the building profile from meta data
    building_data = BuildingMetadata[BuildingMetadata['building_id']
                                     == BuildingName].iloc[0]
    # Check the building has this meter installed.
    if str(building_data[MeterName]) == 'True':

        StartDate = datetime.strptime(Start, '%Y-%m-%d')
        EndDate = datetime.strptime(End, '%Y-%m-%d')

        # Get the Data
        data = get_meter_data_for_building(MeterName, BuildingName)
        # Filter by Date
        data = data[data['timestamp'] >= StartDate]
        data = data[data['timestamp'] < EndDate]
        # Calculate year, we always filter by that.
        data['Year'] = data.timestamp.dt.year
        data = data.compute()
        # Calculate the group for the agg unit of time
        if AggLevel == 'None':
            data = data.rename(columns={'timestamp': 'Date'})
        else:
            if AggLevel == 'Quarter':
                data['Date'] = data['Year'].astype(
                    str) + '-Q' + data.timestamp.dt.quarter.astype(str)
            elif AggLevel == 'Week':
                data['YearWeek'] = data['Year'].astype(
                    str) + '-' + data.timestamp.dt.strftime('%U')
                data['Date'] = data['YearWeek'].apply(
                    lambda x: datetime.strptime(x + '-1', "%Y-%W-%w"))
            else:
                data['Day'] = 1
                data['Month'] = data.timestamp.dt.month
                data['Date'] = pd.to_datetime(data[['Year', 'Month', 'Day']])

            #Group and aggregate
            data = data[['Year', 'Date', MeterName]].groupby(
                ['Year', 'Date'], as_index=False)
            if aggFunction == 'Avg':
                data = data.mean()
            elif aggFunction == 'Max':
                data = data.max()
            elif aggFunction == 'Min':
                data = data.min()
            else:
                data = data.sum()

        # Rename the agg column
        data = data.rename(columns={MeterName: (
            ValuesColumnName + ' Consumption')})

        # generate the
        fig = px.line(data, x='Date',
                      y=ValuesColumnName + ' Consumption', markers=True,
                      template="simple_white", line_shape="spline", render_mode="svg")

        fig['data'][0]['showlegend'] = True
        fig['data'][0]['line']['color']= "yellowgreen"
        #fig['data'][0]['name'] = 'Building: ' + \
            #str(BuildingName).replace("_", " ")  # Either we show this
        fig['data'][0]['name']= 'Building: ' + \
             str(BuildingName).split("_")[-1] # or this

        fig.update_layout(legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        ))
        # fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
        fig.update_yaxes(ticksuffix=MeasurementUnit)
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

        return [fig, {'display': 'block'}]
    else:
        return [no_update, {'display': 'none'}]

# endregion

# region Supporting Functions
def FormatOptions(Items: list):
    optionsList = list()
    for item in Items:
        label = str(item).replace("_", " ").title()
        optionsList.append({'label': label, 'value': str(item)})
    return optionsList
# endregion
