# import packages
from dash import Dash, dcc, html, Input, Output, callback, State
import dash_bootstrap_components as dbc

# logo
ENERGYHUB_LOGO = '/assets/images/logo/green_energyhub_logo.png'

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


def CreateContainer(AboutTeam=False):
    conatinerItems = list()
    conatinerItems.extend([
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [dbc.Col(html.Img(src=ENERGYHUB_LOGO,
                                  height="50px", width="200px", ))],
                className="g-0",
            ),
            href='/home'
        ),
        dbc.NavItem(dbc.NavLink("Home", href="/home", active=True,
                    class_name='', style=NAVLINKS_STYLE)),
        dbc.NavItem(dbc.NavLink("Overview", active=True,
                    href="/data_overview", style=NAVLINKS_STYLE)),
        dbc.NavItem(dbc.NavLink(
            "Energy Profile", href="/buildings", style=NAVLINKS_STYLE)),
        dbc.NavItem(dbc.NavLink(
            "Forecast", href="/forecast", style=NAVLINKS_STYLE)),
    ])

    if AboutTeam:
        conatinerItems.append(dbc.NavItem(dbc.NavLink(
            "Team", href="/home#TeamCards", external_link=True, style=NAVLINKS_STYLE)),)

    conatinerItems.extend([dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                           dbc.Collapse(
        id="navbar-collapse",
        is_open=False,
        navbar=True,
    ), 
    ])


    return conatinerItems

def CreateLayout(AboutTeam):
    conatinerItems = CreateContainer(AboutTeam)
    layout = dbc.Navbar(
    dbc.Container(
        conatinerItems
    ),
    color="light",
    dark=False,
    className='navbar sticky-top',
    )

    return layout

# add callback for toggling the collapse on small screens
@callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],)
def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open