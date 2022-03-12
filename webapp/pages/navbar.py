 # import packages
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

# logo
ENERGYHUB_LOGO = '/assets/images/Energy Hub-logos_black_cropped.png'

NAVLINKS_STYLE = {
        'display': 'block',
        'text-align': 'center',
        'padding': '16px 60px',
        'text-decoration': 'none',
        'color': 'black',
        'position': 'sticky',
        'font-size': '25px',
        'font-family': 'serif'
}

# set up the nav layout
layout = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [dbc.Col(html.Img(src=ENERGYHUB_LOGO, height="50px", width="200px", ))],
                    className="g-0",
                ),
                href='/home'
            ),
            dbc.NavItem(dbc.NavLink("Home", href="/home",active=True,class_name='', style=NAVLINKS_STYLE)),
            dbc.NavItem(dbc.NavLink("Data Overview", active=True,href="/data_overview", style=NAVLINKS_STYLE)),
            dbc.NavItem(dbc.NavLink("Forecast", href="#", style=NAVLINKS_STYLE)),
            dbc.NavItem(dbc.NavLink("About the team", href="#", style=NAVLINKS_STYLE)),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="light",
    dark=False,
)