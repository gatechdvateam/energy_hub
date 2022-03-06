from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import navbar, home, page1, page2
import os

cdn_Style_Sheets = [dbc.themes.BOOTSTRAP]

cdn_Scripts = []

#Create the app and request a reference external style sheets and scripts.
app = Dash(__name__, suppress_callback_exceptions=True, \
    external_stylesheets=cdn_Style_Sheets,external_scripts=cdn_Scripts)

#Required for Azure Deployment
server = app.server

app.layout = html.Div([
    # represents the browser address bar and doesn't render anything
    dcc.Location(id='url', refresh=False),
    #This Navbar should show on all pages
    navbar.layout,
    # This is a container that will contain content from pages in other files.
    html.Div(id='page-content',className='container')
])

#Route to different pages
@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    elif pathname == '/page2':
        return page2.layout
    else:
        return home.createLayout()

#Runs a server for development
if __name__ == '__main__':
    app.run_server(debug=True)