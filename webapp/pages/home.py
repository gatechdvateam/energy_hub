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
card_siham = html.Div([
        dbc.Card([dbc.Col(
                    dbc.CardImg(
                        src="assets/images/siham.png",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Siham Elmali", className="card-title", style=CARD_TEXT_STYLE),
                            html.P(
                                "Siham Elmali is a data scientist working at Intel.\
                                She has a BS/MS in ECE from Johns Hopkins University.\
                                She is currently pursuing a masters in Analytics at Georgia Tech.",
                                className="card-text",
                            ),
                            ]
                    ),
                    className="col-md-8",
                ),
            ]
        )
    ],
    className="mb-4 border-0",
    style={"maxWidth": "540px"},
    )
    

card_hassan = html.Div([
        dbc.Card([
                dbc.Col(
                    dbc.CardImg(
                        src="assets/images/random.jpg",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Hassan Mousa", className="card-title", style=CARD_TEXT_STYLE),
                            html.P(
                                "Hassan is a data scientist working at NYU.\
                                He has a BS/MS in ECE from Johns Hopkins University. He is currently\
                                pursuing a masters in Analytics at Georgia Tech.",
                                className="card-text",
                            ),
                            ]
                    ),
                    className="col-md-8",
                ),
            ]
        ),
        ],
    className="mb-4 border-0",
    style={"maxWidth": "540px"},
)

card_mai = html.Div([
        dbc.Card([
                dbc.Col(
                    dbc.CardImg(
                        src="assets/images/random.jpg",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Mai Colman", className="card-title", style=CARD_TEXT_STYLE),
                            html.P(
                                "Mai is a data scientist working at NYU.\
                                She has a BS/MS in ECE from Johns Hopkins University. He is currently\
                                pursuing a masters in Analytics at Georgia Tech.",
                                className="card-text",
                            ),
                            ]
                    ),
                    className="col-md-8",
                ),
            ]
        )
        ],
    className="mb-4 border-0",
    style={"maxWidth": "540px"},
)

card_mert = html.Div([
        dbc.Card([
                dbc.Col(
                    dbc.CardImg(
                        src="assets/images/mert-real.jpg",
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4("Mert", className="card-title", style=CARD_TEXT_STYLE),
                            html.P(
                                "Mert is a data scientist working at NYU.\
                                He has a BS/MS in ECE from Johns Hopkins University. He is currently\
                                pursuing a masters in Analytics at Georgia Tech.",
                                className="card-text",
                            ),
                            ]
                    ),
                    className="col-md-8",
                ),
            ]
        )
        ],
    className="mb-4 border-0",
    style={"maxWidth": "540px", "border": "none", "outline":"none"},
)


siham_hassan = html.Div(children=[card_siham, card_hassan], className="row")
mai_mert = html.Div(children=[card_mai, card_mert], className="row")

layout = html.Div([html.Div([
        html.Div([], className='col-md-6', style={'marginTop': '10px'},)
    ], className='row')])
layout.children.append(carousel)
layout.children.append(html.Br())

layout.children.append(html.H2("About the team"))
layout.children.append(html.Br())
layout.children.append(siham_hassan)
layout.children.append(html.Br())
layout.children.append(mai_mert)