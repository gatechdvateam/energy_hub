from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import data_overview, navbar, home, buildings, elec_forecast


# cdn_Style_Sheets = ['assets/css/bootstrap.css']
bootstrap_sheet = ['https://bootswatch.com/5/flatly/bootstrap.min.css']

cdn_Scripts = []

#Create the Dash_App and request a reference external style sheets and scripts.
Dash_App = Dash(__name__, suppress_callback_exceptions=True, \
    external_stylesheets=bootstrap_sheet,external_scripts=cdn_Scripts,title='Energy Hub')

#Required for Azure Deployment
server = Dash_App.server

Dash_App.layout = html.Div([
    # represents the browser address bar and doesn't render anything
    dcc.Location(id='url', refresh=False),
    #This Navbar should show on all pages
    html.Div(id='page-header'),
    # This is a container that will contain content from pages in other files.
    
    html.Div(id='page-content',className='container-fluid'),
    html.Footer([html.Br(),
        html.Div("© 2022 Copyright: Energy Hub Team", id='footer-text', 
                style={'textAlign': 'center', 'font-size':'25px', 'font-family': 'serif'},
                className="bg-light text-inverse text-center")]),
    html.Div(id='EmptyDiv')
])

#Route to different pages
@callback(Output('page-content', 'children'),
          Output('page-header', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):

    if pathname == '/data_overview':
        return data_overview.createLayout(),navbar.CreateLayout()
    elif pathname == '/buildings':
        return buildings.createLayout(),navbar.CreateLayout()
    elif pathname == '/forecast':
        return elec_forecast.createLayout(),navbar.CreateLayout()
    elif pathname == '/home':
        return home.home_layout(),navbar.CreateLayout()
    else:
        return home.home_layout(),navbar.CreateLayout()

#Runs a server for development
if __name__ == '__main__':
    Dash_App.run_server(debug=True,host='127.0.0.1', port=80)