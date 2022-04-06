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
    title = html.H2('ELectricity Forecast and Normalization',
                    style={"text-align": "center"})

    row1 = dbc.Row(CreateFilters())
    row2 = dbc.Row(CreateVisuals())
    row3 = dbc.Row(dbc.Col(html.P(children=[
        html.Br(),
        '*Date filter will reset if start date is > end date.',
        html.Br(),
        '*Filter will also reset when "None" is selected in aggregation level and end date is greater than start date by 10 days.',
        html.Br(),
        '*Not supported for aggregation level None.'
    ], className='text-warning'), md=12))

    return [html.H2("Building Electricty Forecast", className='text-center'), html.Br(), 
            row1,
            html.Br(), row2, row3]


def CreateFilters():

    # make a copy of the data
    building_meta = BuildingMetadata.copy()

    # Create the filters column
    columns = []

    # select Timezone/location
    timezone = CreateSelect(
        list(building_meta['timezone'].unique()), 'FP_TimezoneFilter')
    columns.append(
        dbc.Col([dbc.Label("Time Zone:"), html.Br(), timezone, html.Br()], lg=2))

    # select primary usage
    primary_usage = CreateSelect(
        list(building_meta['primary_space_usage'].unique()), 'FP_UsageFilter')
    columns.append(dbc.Col(
        [dbc.Label("Primary Usage:"), html.Br(), primary_usage, html.Br()], lg=2))

    # select building size
    building_size = CreateSelect(
        list(building_meta['size'].unique()), 'FP_BuildingSizeFilter')
    columns.append(dbc.Col(
        [dbc.Label("Building Size:"), html.Br(), building_size, html.Br()], lg=2))

    # select a building (testing multiple filtering)
    # column.children.extend(
    #     [dbc.Label("Select 2 Buildings to compare****:"), html.Br()])

    buildings = list(building_meta['building_id'].unique())

    building_1 = CreateSelect(
        buildings, 'FP_BuildingFilter1', 'Bull_lodging_Travis', False, True)
    columns.append(dbc.Col(
        [dbc.Label("Building #1:"), html.Br(), building_1, html.Br()], lg=2))

    building_2 = CreateSelect(
        buildings, 'FP_BuildingFilter2', 'Rat_office_Colby', False, True)
    columns.append(dbc.Col(
        [dbc.Label("Building #2:"), html.Br(), building_2, html.Br()], lg=2))

    # select Aggregation Level
    level = CreateSelect(['Month', 'Quarter', 'Week', 'None'],
                         'FP_AggLevelFilter', 'None')
    columns.append(dbc.Col(
        [dbc.Label("Aggregation Level:"), html.Br(), level, html.Br()], lg=2))

    # select Aggregation Type
    ty_pe = CreateSelect(['Sum', 'Avg', 'Max', 'Min'],
                         'FP_AggTypeFilter', 'Sum')
    columns.append(dbc.Col(
        [dbc.Label("Aggregation Type:"), html.Br(), ty_pe, html.Br()], lg=2))

    # select Dates
    dates = dcc.DatePickerRange(
        id='FP_DateFilter',
        min_date_allowed=date(2016, 1, 1),
        max_date_allowed=date(2017, 12, 31),
        start_date=date(2017, 1, 1),
        end_date=date(2017, 1, 2)
    )
    columns.append(
        dbc.Col([dbc.Label("Start & End Dates: *:"), html.Br(), dates, html.Br()], lg=2))

    # Apply Filter
    columns.append(dbc.Col([ html.Br(),html.Button('Apply Filters', id='ApplyFilters', style={"background-color": "yellowgreen", "color": "black", "width": "150px"},
                                        n_clicks=0, className="btn btn-primary"), html.Br()], lg=2))

    return columns


def CreateVisuals():
    """
        This function is responsible for creating the charts area.
    """
    # Create Charts
    electricity_plot1 = dcc.Loading(
        dcc.Graph(id='FP_electricity1'), type='default')
    electricity_plot2 = dcc.Loading(
        dcc.Graph(id='FP_electricity2'), type='default')

    norm_electricity_plot1 = dcc.Loading(
        dcc.Graph(id='FP_electricity_norm1'), type='default')
    norm_electricity_plot2 = dcc.Loading(
        dcc.Graph(id='FP_electricity_norm2'), type='default')

    column1 = dbc.Col([electricity_plot1, norm_electricity_plot1], md=6)
    column2 = dbc.Col([electricity_plot2, norm_electricity_plot2], md=6)

    return [column1, column2]
# endregion


# region Callbacks for chart updates

# Define the list of inputs that affects the chart re render one time here rather than repeat.
filterInputList = {"Values": {
    "Building1": State('FP_BuildingFilter1', 'value'),
    "Building2": State('FP_BuildingFilter2', 'value'),
    "StartDate": State('FP_DateFilter', 'start_date'),
    "EndDate": State('FP_DateFilter', 'end_date'),
    "AggLevel": State('FP_AggLevelFilter', 'value'),
    "AggType": State('FP_AggTypeFilter', 'value'),
    "NC": Input('ApplyFilters', 'n_clicks')
}}

@callback(
    output=[Output('FP_electricity1', 'figure'),
            Output('FP_electricity1', 'style'), ],
    inputs=filterInputList)
def plot1_electricity(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building1"], 'electricity', 'Electricity',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'])

@callback(
    output=[Output('FP_electricity2', 'figure'),
            Output('FP_electricity2', 'style'), ],
    inputs=filterInputList)
def plot2_electricity(Values):
    return CreateTimeChart(Values["StartDate"], Values["EndDate"], Values["Building2"], 'electricity', 'Electricity',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'])

@callback(
    output=[Output('FP_electricity_norm1', 'figure'),
            Output('FP_electricity_norm1', 'style'), ],
    inputs=filterInputList)
def plot_norm_electricity1(Values):
    return CreateNormalizedChart(Values["StartDate"], Values["EndDate"], Values["Building1"], 'electricity', 'Electricity',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'])

@callback(
    output=[Output('FP_electricity_norm2', 'figure'),
            Output('FP_electricity_norm2', 'style'), ],
    inputs=filterInputList)
def plot_norm_electricity2(Values):
    return CreateNormalizedChart(Values["StartDate"], Values["EndDate"], Values["Building2"], 'electricity', 'Electricity',
                           AggLevel=Values['AggLevel'], aggFunction=Values['AggType'])


# Define Outputs here
filtersUpdateOutputs = [
    Output('FP_BuildingFilter1', 'options'),
    Output('FP_BuildingFilter1', 'value'),
    Output('FP_BuildingFilter2', 'options'),
    Output('FP_BuildingFilter2', 'value'),
    Output('FP_UsageFilter', 'options'),
    Output('FP_UsageFilter', 'value'),
    Output('FP_BuildingSizeFilter', 'options'),
    Output('FP_BuildingSizeFilter', 'value'),
    Output('FP_TimezoneFilter', 'options'),
    Output('FP_TimezoneFilter', 'value')]
# Define Inputs here
filtersUpdateInputs = [Input('FP_TimezoneFilter', 'value'),
                       Input('FP_UsageFilter', 'value'),
                       Input('FP_BuildingSizeFilter', 'value')]


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
    outputs.extend([BuildingOptions, Buildingval])

    # if the filter was not updated, i.e. the user didn't play with this value
    # We get the list of available values for all filters below.
    if FilterID != 'FP_UsageFilter':
        UsageOptions = list(buildings['primary_space_usage'].unique())
        outputs.extend([UsageOptions, no_update])
    else:
        outputs.extend([no_update, no_update])

    if FilterID != 'FP_BuildingSizeFilter':
        SizeOptions = list(buildings['size'].unique())
        outputs.extend([SizeOptions, no_update])
    else:
        outputs.extend([no_update, no_update])

    if FilterID != 'FP_TimezoneFilter':
        TimezoneOptions = list(buildings['timezone'].unique())
        outputs.extend([TimezoneOptions, no_update])
    else:
        outputs.extend([no_update, no_update])

    return outputs
# endregion

# region support functions to create charts and filters


@callback(
    Output('FP_DateFilter', 'start_date'),
    Output('FP_DateFilter', 'end_date'),
    Input('FP_DateFilter', 'start_date'),
    Input('FP_DateFilter', 'end_date'),
    Input('FP_AggLevelFilter', 'value'),
    prevent_initial_call=True)
def RestrictDays(StartDate, EndDate, AggLevel):
    # Parse Dates
    Start = datetime.strptime(StartDate, '%Y-%m-%d')
    End = datetime.strptime(EndDate, '%Y-%m-%d')

    # Create Default Dates
    DefaultStart = date(2017, 1, 1)
    DefaultEnd = date(2017, 12, 31)

    # Limit to 7 Days.
    if AggLevel == "None":
        DefaultEnd = date(2017, 1, 7)
        if Start > End:
            return DefaultStart, DefaultEnd
        delta = End - Start
        if delta.days > 10:
            return DefaultStart, DefaultEnd
        return no_update, no_update

    # Just verify that end date is not greater than start.
    else:
        if Start > End:
            return DefaultStart, DefaultEnd
        return no_update, no_update
# endregion


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

# region Chart
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
        data, _ = get_normalized_date(BuildingName)

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
            data = data[['Year', 'Date', 'y_trues']].groupby(
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
        data = data.rename(columns={'y_trues': (
            ValuesColumnName + ' Consumption')})

        # generate the
        fig = px.line(data, x='Date',
                      y=ValuesColumnName + ' Consumption', markers=True,
                      template="simple_white", line_shape="spline", render_mode="svg")

        fig['data'][0]['showlegend'] = True
        fig['data'][0]['line']['color'] = "yellowgreen"
        # fig['data'][0]['name'] = 'Building: ' + str(BuildingName).replace("_", " ")  # Either we show this
        fig['data'][0]['name'] = 'Building: ' + \
            str(BuildingName).split("_")[-1]  # or this

        fig.update_layout(legend=dict(
            yanchor="top",
            y=1,
            xanchor="right",
            x=0.01
        ))
        # fig.add_trace(dict(color='green', width=4, dash='dash'))
        # fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
        fig.update_yaxes(ticksuffix=MeasurementUnit)
        fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
        fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

        return [fig, {'display': 'block'}]
    else:
        return [no_update, {'display': 'none'}]

# endregion

# region Chart
def CreateNormalizedChart(Start: str, End: str, BuildingName: str, MeterName: str,
                    ValuesColumnName: str, MeasurementUnit: str = " kW", AggLevel: str = 'Month', aggFunction='Sum'):
    """
    Function that checks if the meter data is available for a given building and
    creates a normalized electricity chart for that.
    """

    # Load the building profile from meta data
    building_data = BuildingMetadata[BuildingMetadata['building_id']
                                     == BuildingName].iloc[0]
    # Check the building has this meter installed.
    if str(building_data[MeterName]) == 'True':

        StartDate = datetime.strptime(Start, '%Y-%m-%d')
        EndDate = datetime.strptime(End, '%Y-%m-%d')

        # Get the Data
        data, _ = get_normalized_date(BuildingName)
        # Filter by Date
        data = data[data['timestamp'] >= StartDate]
        data = data[data['timestamp'] < EndDate]

        # Calculate year, we always filter by that.
        data['Year'] = data.timestamp.dt.year
  
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
            data = data[['Year', 'Date', "y_norms"]].groupby(
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
        data = data.rename(columns={'y_norms': ( 'Normalized ' + ValuesColumnName +  ' Consumption')})

        # max_r2 = data.groupby(["norm_output_" + BuildingName], sort=False)['R2'].max()
        # generate the
        fig = px.line(data, x='Date',
                      y='Normalized ' + ValuesColumnName +  ' Consumption', markers=True,
                      template="simple_white", line_shape="spline", render_mode="svg")

        fig['data'][0]['showlegend'] = True
        fig['data'][0]['line']['color'] = "slateblue"
        fig['data'][0]['name'] = 'Building: ' + \
            str(BuildingName).split("_")[-1]

        fig.update_layout(legend=dict(
            yanchor="top",
            y=1,
            xanchor="right",
            x=0.01
        ))
        # fig.add_trace(dict(color='green', width=4, dash='dash'))
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
