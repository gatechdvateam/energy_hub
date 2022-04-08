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
    layout =list()
    title = html.H2('ELectricity Forecast and Normalization',className='text-center')

    row1 = dbc.Row(CreateFilters())
    row2 = dbc.Row(CreateForecastVisuals())
    row3 = dbc.Row(CreateNormilizationVisuals())
    row4 = dbc.Row(dbc.Col(html.P(children=[
        html.Br(),
        '*Not supported for aggregation level None.'
    ], className='text-warning'), md=12))

    layout.append(title)
    layout.append(html.Br())
    layout.append(row1)
    layout.append(html.Br())
    layout.append(html.H3('Consumption Forecast'))
    layout.append(html.P('Forecast data is available for one week only.'))
    layout.append(row2)
    layout.append(html.Br())
    layout.append(html.H3('Normalized Consumption'))
    layout.append(row3)
    layout.append(html.Br())
    layout.append(row4)

    return layout


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

    #Select Buildings
    buildings = list(building_meta['building_id'].unique())

    building_1 = CreateSelect(
        buildings, 'FP_BuildingFilter1', 'Bear_education_Maryjane', False, True)
    columns.append(dbc.Col(
        [dbc.Label("Building #1:"), html.Br(), building_1, html.Br()], lg=2))

    building_2 = CreateSelect(
        buildings, 'FP_BuildingFilter2', 'Bear_education_Babara', False, True)
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
        [dbc.Label("Aggregation Type: *"), html.Br(), ty_pe, html.Br()], lg=2))

    # Sync Axis
    sync = CreateSelect(['Yes','No'],'FP_Sync', 'Yes')

    columns.append(dbc.Col(
        [dbc.Label("Sync Y Axis: "), html.Br(), sync, html.Br()], lg=2))
    
    # Normalized Elements
    normElem = CreateSelect(['Actual','Predicted','Weather Normalized'],'NormElem',MultipleValues=True)

    columns.append(dbc.Col(
        [dbc.Label("Normalized Charts Values: "), html.Br(), normElem, html.Br()], lg=2))

    # select Dates
    dates = dcc.DatePickerRange(
        id='FP_DateFilter',
        min_date_allowed=date(2016, 1, 1),
        max_date_allowed=date(2017, 12, 31),
        start_date=date(2017, 12, 25),
        end_date=date(2017, 12, 28)
    )
    columns.append(
        dbc.Col([dbc.Label("Start & End Dates: *"), html.Br(), dates, html.Br()], lg=2))

    # Apply Filter
    columns.append(dbc.Col([html.Br(), html.Button('Apply Filters', id='ApplyFilters', style={"background-color": "yellowgreen", "color": "black", "width": "150px"},
                                                   n_clicks=0, className="btn btn-primary"), html.Br()], lg=2))

    return columns

def CreateForecastVisuals():
    """
        This function is responsible for creating the charts area.
    """
    # Create Charts
    forecast_plot1 = dcc.Loading(
        dcc.Graph(id='forecast_plot1'), type='default')
    forecast_plot2 = dcc.Loading(
        dcc.Graph(id='forecast_plot2'), type='default')

    column1 = dbc.Col(forecast_plot1, md=6)
    column2 = dbc.Col(forecast_plot2, md=6)

    return [column1, column2]

def CreateNormilizationVisuals():
    """
        This function is responsible for creating the charts area.
    """
    # Create Charts
    norm_electricity_plot1 = dcc.Loading(
        dcc.Graph(id='FP_electricity_norm1'), type='default')
    norm_electricity_plot2 = dcc.Loading(
        dcc.Graph(id='FP_electricity_norm2'), type='default')

    column1 = dbc.Col(norm_electricity_plot1, md=6)
    column2 = dbc.Col(norm_electricity_plot2, md=6)

    return [column1, column2]
# endregion

# region Chart Callbacks

# Define the list of inputs that affects the chart re render one time here rather than repeat.
filterInputList = {"Values": {
    "Building1": State('FP_BuildingFilter1', 'value'),
    "Building2": State('FP_BuildingFilter2', 'value'),
    "StartDate": State('FP_DateFilter', 'start_date'),
    "EndDate": State('FP_DateFilter', 'end_date'),
    "AggLevel": State('FP_AggLevelFilter', 'value'),
    "AggType": State('FP_AggTypeFilter', 'value'),
    "Sync": State('FP_Sync', 'value'),
    "NormElem": State('NormElem', 'value'),
    "NC": Input('ApplyFilters', 'n_clicks'),
}}

@callback(
    output=[Output('forecast_plot1', 'figure'),
            Output('forecast_plot1', 'style'),
            Output('forecast_plot2', 'figure'),
            Output('forecast_plot2', 'style'), ],
    inputs=filterInputList)
def plot_forecast(Values):
    #We need to load both datasets in one call here. This is a very special case because we are doing a comparison.
    #In terms for performance this is not the fastest approach but it is the only way we have now.
    List1 = CreateForecastChart(Values["StartDate"], Values["EndDate"], Values["Building1"], 'Electricity',
                                 AggLevel=Values['AggLevel'], aggFunction=Values['AggType'])
                                 
    List2 = CreateForecastChart(Values["StartDate"], Values["EndDate"], Values["Building2"], 'Electricity',
                                 AggLevel=Values['AggLevel'], aggFunction=Values['AggType'])
    if Values['Sync'] =='Yes':
        #Get the minimum value from both datasets or 0 if min value >0.
        Min = min([List1[2],List2[2]])
        Min = Min - Min*0.02
        #get the maximum value from both dataset.
        Max = max([List1[3],List2[3]])
        Max = Max + Max*0.02
        #Update the charts
        List1[0].update_layout(yaxis_range=[Min,Max])
        List2[0].update_layout(yaxis_range=[Min,Max])

    #The create normalized chart will return extra varibles which we don't need so we pick the first 2.
    output = List1[0:2]
    output.extend(List2[0:2])
    return output
# endregion


@callback(
    output=[Output('FP_electricity_norm1', 'figure'),
            Output('FP_electricity_norm1', 'style'),
            Output('FP_electricity_norm2', 'figure'),
            Output('FP_electricity_norm2', 'style'), ],
    inputs=filterInputList)
def plot_norm_electricity(Values):
    #We need to load both datasets in one call here. This is a very special case because we are doing a comparison.
    #In terms for performance this is not the fastest approach but it is the only way we have now.
    List1 = CreateNormalizedChart(Values["StartDate"], Values["EndDate"], Values["Building1"], 'Electricity',
                                 AggLevel=Values['AggLevel'], aggFunction=Values['AggType'],Elements=Values['NormElem'])
                                 
    List2 = CreateNormalizedChart(Values["StartDate"], Values["EndDate"], Values["Building2"], 'Electricity',
                                 AggLevel=Values['AggLevel'], aggFunction=Values['AggType'],Elements=Values['NormElem'])
    if Values['Sync'] =='Yes':
        #Get the minimum value from both datasets or 0 if min value >0.
        Min = min([List1[2],List2[2]])
        Min = Min - Min*0.02
        #get the maximum value from both dataset.
        Max = max([List1[3],List2[3]])
        Max = Max + Max*0.02
        #Update the charts
        List1[0].update_layout(yaxis_range=[Min,Max])
        List2[0].update_layout(yaxis_range=[Min,Max])

    #The create normalized chart will return extra varibles which we don't need so we pick the first 2.
    output = List1[0:2]
    output.extend(List2[0:2])
    return output
# endregion

# region Filters callbacks
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

# region Select Maker
def CreateSelect(ItemsList, Name, DefaultValue=None, Optional=True, Format=False,MultipleValues=False):
    """
    Function to create select lists.
    """
    optionsList = None
    if(Format):
        optionsList = FormatOptions(ItemsList)
    else:
        optionsList = ItemsList

    return dcc.Dropdown(optionsList, DefaultValue, id=Name, clearable=Optional,multi=MultipleValues)
# endregion

# region Charts
def CreateForecastChart(Start: str, End: str, BuildingName: str, ValuesColumnName: str,
                           MeasurementUnit: str = " kW", AggLevel: str = 'Month', aggFunction='Sum'):
    """
    Function that checks if the meter data is available for a given building and
    creates a normalized electricity chart for that.
    """
    StartDate = datetime.strptime(Start, '%Y-%m-%d')
    EndDate = datetime.strptime(End, '%Y-%m-%d')

    # Get the Data
    data = get_forecast_for_building(BuildingName)
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
        data = data[['Year', 'Date', "electricity", "predictions"]].groupby(
            ['Year', 'Date'], as_index=False)
        if aggFunction == 'Avg':
            data = data.mean()
        elif aggFunction == 'Max':
            data = data.max()
        elif aggFunction == 'Min':
            data = data.min()
        else:
            data = data.sum()

    #Form the names for the columns.
    elec_orig = 'Actual ' + ValuesColumnName + ' Consumption'
    elec_forc = 'DL Forecast ' + ValuesColumnName + ' Consumption'
    
    # Rename the agg columns
    data = data.rename(columns={'electricity': elec_orig})
    data = data.rename(columns={'predictions': elec_forc})
    yElements=[elec_orig,elec_forc]

    #Calculate Min across y Elements.
    MinVal = data[yElements].min(axis=1).min()
    #Calculate Max across y Elements.
    MaxVal = data[yElements].max(axis=1).max()

    #Create the Chart
    fig = px.line(data, x='Date',
                  y=yElements, markers=True, 
                  template="simple_white", line_shape="spline", render_mode="svg")

    fig['data'][0]['showlegend'] = True

    # fig['data'][0]['name'] = 'Building: ' + \
    #     str(BuildingName).split("_")[-1]

    fig.update_layout(legend=dict(
        yanchor="bottom",
        y=0.99,
        xanchor="left",
        x=0.01,

    ), legend_title='Building: '+BuildingName.split('_')[-1])

    fig.update_layout(
        legend=dict(
            title_font_family="Calibri",
            font=dict(
                family="Calibri",
                size=16,
                color="black"
            ),
            bgcolor="whitesmoke",
            bordercolor="lightBlue",
            borderwidth=1
        )
    )
    # fig.add_trace(dict(color='green', width=4, dash='dash'))
    # fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    fig.update_yaxes(ticksuffix=MeasurementUnit)
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return [fig, {'display': 'block'},MinVal,MaxVal]


def CreateNormalizedChart(Start: str, End: str, BuildingName: str, ValuesColumnName: str,
                           MeasurementUnit: str = " kW", AggLevel: str = 'Month', aggFunction='Sum',Elements=None):
    """
    Function that creates a normalized electricity chart for the building.
    """
    StartDate = datetime.strptime(Start, '%Y-%m-%d')
    EndDate = datetime.strptime(End, '%Y-%m-%d')

    # Get the Data
    data = get_normalized_date(BuildingName)
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
        data = data[['Year', 'Date', "y_trues", "y_preds", "y_norms"]].groupby(
            ['Year', 'Date'], as_index=False)
        if aggFunction == 'Avg':
            data = data.mean()
        elif aggFunction == 'Max':
            data = data.max()
        elif aggFunction == 'Min':
            data = data.min()
        else:
            data = data.sum()

    #Form the names for the columns.
    elec_norm = 'Weather-Normalized ' + ValuesColumnName + ' Consumption'
    elec_orig = 'Actual ' + ValuesColumnName + ' Consumption'
    elec_pred = 'Predicted ' + ValuesColumnName + ' Consumption'
    
    # Rename the agg columns
    data = data.rename(columns={'y_norms': elec_norm})
    data = data.rename(columns={'y_trues': elec_orig})
    data = data.rename(columns={'y_preds': elec_pred})

    #Enable the Y elements Filter
    yElements=[]
    if Elements is None or len(Elements)==0:
        yElements = [elec_orig, elec_pred, elec_norm]
    else:
        if 'Actual' in Elements:
            yElements.append(elec_orig)
        if 'Predicted' in Elements:
            yElements.append(elec_pred)
        if 'Weather Normalized' in Elements:
            yElements.append(elec_norm)

    #Calculate Min across y Elements.
    MinVal = data[yElements].min(axis=1).min()
    #Calculate Max across y Elements.
    MaxVal = data[yElements].max(axis=1).max()

    #Create the Chart
    fig = px.line(data, x='Date',
                  y=yElements, markers=True, 
                  template="simple_white", line_shape="spline", render_mode="svg")

    fig['data'][0]['showlegend'] = True

    #Fix the line colors to prevent color changes when user selects 1 or 2 of the 3 elements.
    for x in fig['data']:
        x['line']['color'] = Calculate_Color(x['name'])

    # fig['data'][0]['name'] = 'Building: ' + \
    #     str(BuildingName).split("_")[-1]

    fig.update_layout(legend=dict(
        yanchor="bottom",
        y=0.99,
        xanchor="left",
        x=0.01,

    ), legend_title='Building: '+BuildingName.split('_')[-1])
    
    fig.update_layout(
        legend=dict(
            title_font_family="Calibri",
            font=dict(
                family="Calibri",
                size=16,
                color="black"
            ),
            bgcolor="whitesmoke",
            bordercolor="lightBlue",
            borderwidth=1
        )
    )
    # fig.add_trace(dict(color='green', width=4, dash='dash'))
    # fig.update_layout(plot_bgcolor='#f9f9f9', paper_bgcolor='#f9f9f9')
    fig.update_yaxes(ticksuffix=MeasurementUnit)
    fig.update_xaxes(showline=True, linewidth=2, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='black')

    return [fig, {'display': 'block'},MinVal,MaxVal]


# endregion

# region Supporting Functions

def FormatOptions(Items: list):
    optionsList = list()
    for item in Items:
        label = str(item).replace("_", " ").title()
        optionsList.append({'label': label, 'value': str(item)})
    return optionsList

def Calculate_Color(name: str):
    color = {'Actual Electricity Consumption': 'blue',
             'Predicted Electricity Consumption': 'orange',
             'Weather-Normalized Electricity Consumption': 'green'}
    return color[name]
# endregion
