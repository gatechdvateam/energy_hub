from turtle import color
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

ENERGYHUB_LOGO = '/assets/energy_hub_logo.png'
layout = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=ENERGYHUB_LOGO, height="40px")),
                        dbc.Col(dbc.NavbarBrand("Energy Hub", className="ms-2")),
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
                href='/home'
            ),
            dbc.NavItem(dbc.NavLink("Data Overview", href="/data_overview",class_name='')),
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