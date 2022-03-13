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
    # 'textAlign': 'center',
    'color': '#191970',
    'font-family': 'serif',
    'font-size': '18px'
}

TEAM_TEXT_STYLE = {
    'color': 'black',
    'font-family': 'serif',
    'font-size': '25px'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': 'black',
    'font-size':'20px'
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
Siham_linkedInURL = 'https://www.linkedin.com/in/siham-elmali'
Mai_linkedInURL = 'https://www.linkedin.com/in/phuongnguyen93'
Mert_linkedInURL = 'https://www.linkedin.com/in/ersozmert'
Hassan_linkedInURL = 'https://www.linkedin.com/in/hassan-abdel-sabour-52362987'

card_content_Siham = [
    dbc.CardHeader("Siham Elmali", style=CARD_TEXT_STYLE),
    dbc.CardBody(
        [
            dbc.CardImg(
                        src="assets/images/team/siham_cropped.jpg",
                        className="img-fluid rounded-start",
                    ),
            html.P(),
            html.P(
                "Siham is a data scientist working at a major semiconductor company in the San Francisco Bay Area.\
                 Siham is an avid sports fan (Soccer, American Football, Hockey, and Tennis.",
                className="card-text", style=TEXT_STYLE,
            ),
            # html.P(['Find her On:'], id='find-me-on', style=TEXT_STYLE),
            html.A([html.Img(src='assets/images/linkedInLogo.png', style={'height': '2rem'})],
                   href=Siham_linkedInURL),
        ]
    ),
]

card_content_mai = [
    dbc.CardHeader("Mai Nguyen", style=CARD_TEXT_STYLE),
    dbc.CardBody(
        [
            dbc.CardImg(
                        src="assets/images/team/mai_cropped.jpg",
                        className="img-fluid rounded-start",
                    ),
            html.P(),
            html.P(
                "Mai is a senior data analyst working for a major company in Atlanta.\
                 She is an avid sports fan (Soccer, American Football, Hockey, and Tennis.",
                className="card-text", style=TEXT_STYLE,
            ),html.Br(),
            # html.P(['Find her On:'], id='find-me-on', style=TEXT_STYLE),
            html.A([html.Img(src='assets/images/linkedInLogo.png', style={'height': '2rem'})],
                   href=Mai_linkedInURL),
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
            html.P(),
            html.P(
                "Mert is a Marine Engineer working for a major cruise line as Energy Optimization & Analytics Manager in Miami.\
                He is an avid sports fan (Soccer, American Football, Hockey, and Tennis.",
                className="card-text", style=TEXT_STYLE,
            ),
            # html.P(['Find him On:'], id='find-me-on', style=TEXT_STYLE),
            html.A([html.Img(src='assets/images/linkedInLogo.png', style={'height': '2rem'})],
                   href=Mert_linkedInURL),
        ]
    ),
]

card_content_hassan = [
    dbc.CardHeader("Hassan Abdel Sabour", style=CARD_TEXT_STYLE),
    dbc.CardBody(
        [
            dbc.CardImg(
                        src="assets/images/team/hassan_cropped.png",
                        className="img-fluid rounded-start",
                    ),
            html.P(),
            html.P(
                "Hassan is a data analyist and full stack developer working at New York University in Abu Dhabi.\
                 He is an avid sports fan (Soccer, American Football, Hockey, and Tennis.",
                className="card-text", style=TEXT_STYLE,
            ),
            # html.P(['Find him On:'], id='find-me-on', style=TEXT_STYLE),
            html.A([html.Img(src='assets/images/linkedInLogo.png', style={'height': '2rem'})],
                   href=Hassan_linkedInURL),
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

footer = html.Footer([
        html.Div("© 2022 Copyright: Energy Hub Team", id='footer-text', 
                style={'textAlign': 'center', 'font-size':'25px', 'font-family': 'serif'},
                className="bg-light text-inverse text-center py-4")])

# adding the cards to the layout
cards = html.Div([cards_row])
layout = html.Div([html.Div([
        html.Div([], className='col-md-6', style={'marginTop': '10px'},)
    ], className='row')])

layout.children.append(carousel)
layout.children.append(html.Br())
layout.children.append(html.H2("About the team", style=TEAM_TEXT_STYLE))
layout.children.append(html.Hr())
layout.children.append(cards)
layout.children.append(html.Br())
layout.children.append(html.Hr())
layout.children.append(footer)