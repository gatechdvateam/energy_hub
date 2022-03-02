from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from pages import page1, page2

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Index", href="/")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Page 1", href="/page1"),
                dbc.DropdownMenuItem("Page 2", href="/page2"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="NavbarSimple",
    brand_href="#",
    color="primary",
    dark=True,
)

app = Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = html.Div([
    # represents the browser address bar and doesn't render anything
    dcc.Location(id='url', refresh=False),
    #Navbar
    navbar,
    
    # represents the browser address bar and doesn't render anything
    html.Div(id='page-content',className='container')
])

#Default Home Page
index_page = html.Div([
    dcc.Link('Go to Page 1', href='/page1'),
    html.Br(),
    dcc.Link('Go to Page 2', href='/page2'),
])

#Route to different pages
@callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/page1':
        out = page1.CreateLayout()
        out.children.insert(0,html.H1('Welcome Baby'))
        return out
    elif pathname == '/page2':
        return page2.layout
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)