# import packages
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


carousel = dbc.Carousel(
    items=[
        {
            "key": "1",
            "src": "/assets/images/background_image_resized2.jpeg",
            "header": "Welcome to Energy Hub"
            # "caption": "and caption",
        },
        {
            "key": "2",
            "src": "/assets/images/background_image_resized2.jpeg",
            # "header": "With header only",
            # "caption": "",
        },
        {
            "key": "3",
            "src": "/assets/images/background_image_resized2.jpeg",
            # "header": "",
            # "caption": "This slide has a caption only",
        },
    ],
    variant="light",
)