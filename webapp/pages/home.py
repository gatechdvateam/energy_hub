# import packages
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
from content import *


def createLayout():
    carousel = dbc.Carousel(
                    items=[
                            {
                                "key": "1",
                                "src": "/assets/images/background/image0_resized.jpeg",
                                "header": "Welcome to Energy Hub",
                                "img_style":{"width":"100%"}
                            },
                            {
                                "key": "2",
                                "src": "/assets/images/background/image1_resized.jpeg",
                            },
                            {
                                "key": "3",
                                "src": "/assets/images/background/image2_resized.jpeg",
                            },
                            
                            {
                                "key": "4",
                                "src": "/assets/images/background/image3_resized.jpeg",
                            },
                        ],
        
                    variant="dark",
                    # controls=True,
                    style=TEXT_STYLE,
                    interval=2000,
                    )
    # adding the carousel to the layout
    layout = dbc.Row([
        dbc.Col([carousel,html.Br()],md=6),
        dbc.Col(dcc.Markdown(HomePageIntro),md=6),
        ],style={'marginTop': '10px'}, className='row')

    return layout
