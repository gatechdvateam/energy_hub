# import packages
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc


CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 0,
    'padding': '20px 10px'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970',
    'font-family': 'serif'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

carousel = html.Div([dbc.Row(dbc.Carousel(
                items=[
                        {
                            "key": "1",
                            "src": "/assets/images/background/image0.jpeg",
                            "header": "Welcome to Energy Hub",
                            "img_style":{"width":"100%"}
                        },
                        {
                            "key": "2",
                            "src": "/assets/images/background/image1.jpeg",
                        },
                        {
                            "key": "3",
                            "src": "/assets/images/background/image2.jpeg",
                        },
                    ],
    
                variant="dark",
                # controls=True,
                style=TEXT_STYLE
                )
            )
        ]
    )
    
    
# making info cards
card_content_Siham = [
    dbc.CardHeader("Siham Elmali", style=CARD_TEXT_STYLE),
    dbc.CardBody(
        [
            dbc.CardImg(
                        src="assets/images/team/siham_cropped.jpg",
                        className="img-fluid rounded-start",
                    ),
            html.P(
                "Siham is a data scientist working at a major semiconductor company in the San Francisco Bay Area.\
                 Siham is an avid sports fan (Soccer, American Football, Hockey, and Tennis.\
                 She is also a space/astronomy enthusiast.",
                className="card-text", style=TEXT_STYLE,
            ),
        ]
    ),
]

card_content_mai = [
    dbc.CardHeader("Mai Colman", style=CARD_TEXT_STYLE),
    dbc.CardBody(
        [
            dbc.CardImg(
                        src="assets/images/team/mai_cropped.jpg",
                        className="img-fluid rounded-start",
                    ),
            html.P(
                "Mai is a senior data analyst working for a major company in Atlanta",
                className="card-text",
            ),
        ]
    ),
]

card_content_mert = [
    dbc.CardHeader("Mert Ersoz", style=CARD_TEXT_STYLE),
    dbc.CardBody(
        [
            dbc.CardImg(
                        src="assets/images/team/mert_cropped.jpg",
                        className="img-fluid rounded-start",
                    ),
            html.P(
                "Mert is a Marine Engineer, working for a major cruise line as Energy Optimization & Analytics Manager in Miami.",
                className="card-text",
            ),
        ]
    ),
]

card_content_hassan = [
    dbc.CardHeader("Hassan Mousa", style=CARD_TEXT_STYLE),
    dbc.CardBody(
        [
            dbc.CardImg(
                        src="assets/images/team/hassan_cropped.png",
                        className="img-fluid rounded-start",
                    ),
            html.P(
                "Hassan is a data analyist and full stack developer working at New York University in Abu Dhabi",
                className="card-text",
            ),
        ]
    ),
]
cards_row = dbc.Row(
    [
        dbc.Col(dbc.Card(card_content_Siham, color="info", outline=True)),
        dbc.Col(dbc.Card(card_content_mai, color="info", outline=True)),
        dbc.Col(dbc.Card(card_content_mert, color="info", outline=True)),
        dbc.Col(dbc.Card(card_content_hassan, color="info", outline=True)),
    ],
    className="mb-4",
)

# adding the cards to the layout
cards = html.Div([cards_row])
layout = html.Div([html.Div([
        html.Div([], className='col-md-6', style={'marginTop': '10px'},)
    ], className='row')])

layout.children.append(carousel)
layout.children.append(html.Br())

layout.children.append(html.H2("About the team", style={'font-family': 'serif'}))
# layout.children.append(html.Br())
layout.children.append(html.Hr())
layout.children.append(cards)