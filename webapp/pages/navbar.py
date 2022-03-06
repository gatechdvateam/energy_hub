from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc

layout = dbc.NavbarSimple(
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
    # brand="NavbarSimple",
    brand_href="/",
    color="primary",
    dark=True,
)