# import packages
from dash import Dash, dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
from data import *
from content import *


def carousel_layout():
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
                                "img_style":{"width":"100%"}
                            },
                            {
                                "key": "3",
                                "src": "/assets/images/background/image2_resized.jpeg",
                                "img_style":{"width":"100%"}
                            },
                            
                            {
                                "key": "4",
                                "src": "/assets/images/background/image3_resized.jpeg",
                                "img_style":{"width":"100%"}
                            },
                        ],
        
                    variant="dark",
                    style=TEXT_STYLE,
                    interval=2000,
                    )
    # adding the carousel to the layout
    layout = dbc.Row([
        dbc.Col([carousel,html.Br()],md=12,
        style={'marginTop': '10px'}, className='row')])

    return layout



def team_layout():
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
                    Siham is an avid sports fan (Soccer, American Football, Hockey, and Tennis).",
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
                    She is an avid sports fan (Soccer, American Football, Hockey, and Tennis).",
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
                    He is an avid sports fan (Soccer, American Football, Hockey, and Tennis).",
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
                    He is an avid sports fan (Soccer, American Football, Hockey, and Tennis).",
                    className="card-text", style=TEXT_STYLE,
                ),
                # html.P(['Find him On:'], id='find-me-on', style=TEXT_STYLE),
                html.A([html.Img(src='assets/images/linkedInLogo.png', style={'height': '2rem'})],
                    href=Hassan_linkedInURL),
            ]
        ),
    ]



    # adding the cards to the layout
    layout = dbc.Row([
            dbc.Col(dbc.Card(card_content_Siham, color="info", outline=True), md=3),
            dbc.Col(dbc.Card(card_content_mai, color="info", outline=True), md=3),
            dbc.Col(dbc.Card(card_content_mert, color="info", outline=True), md=3),
            dbc.Col(dbc.Card(card_content_hassan, color="info", outline=True), md=3)
        ],style={'marginTop': '10px'})
    return layout

def about_us_layout():
    """ This will return a column with text along a map of all sites
        - Talk about the project as a whole
        - Talk about the data
        - Add the map

    """
    general_info = html.Div(dcc.Markdown(random_text), style=TEXT_STYLE, className='col-md-12')

    site_map = html.Div(html.Div(
        [
        # html.H3('Location of all sites', style={'text-align':'center','font-family': 'serif','font-size': '35px'}),
        html.Div(id='MapInput',children=[],style={'display': 'none'}),
        html.Br(),
        dcc.Loading(dcc.Graph(id='site_map', style={'width': '100%', 'height': '50vh', 'margin': "auto", "display": "block"}))
    ], className='col-md-12'
    ), className='row')


    # adding the map and general info to the layout
    layout = dbc.Row([
            dbc.Col([general_info], md=6),
            dbc.Col([site_map], md=6),
        ],style={'marginTop': '10px'})
    return layout




def home_layout():

    carousel = carousel_layout()
    team = team_layout()
    about_us = about_us_layout()
    title=html.H2("The team", style=TEAM_HEADING_STYLE,id='TeamCards')
    title_aboutus=html.H2("Why Energy Hub?", style=TEAM_HEADING_STYLE)

    return [carousel,html.Br(), html.Hr(), title_aboutus, about_us,
            html.Hr(), title,html.Br(),team]


@callback(
    Output('site_map', 'figure'),
    Input('MapInput', 'children'))
def plot_map(df):
    """_summary_

    Args:
        df (_type_): _description_

    Returns:
        _type_: _description_
    """
    #Copy the DataFrame Before making any change. Don't Make changes on global varibales.
    metadata = BuildingMetadata.copy()
    df = metadata[['site_id','longitude','latitude','building_id']]
    df = df.groupby(['site_id','longitude','latitude'],as_index=False).count()
    df = df.rename(columns={'building_id':'Buildings','site_id' : 'Site'})
    fig = px.scatter_geo(df,lon='longitude', lat='latitude',
            color='Site',
            opacity=0.8,
            size='Buildings',
            size_max=50,
            # projection="equirectangular", # Changed Map type
            projection="natural earth",
            #Changed Palette
            color_discrete_sequence=ColorPalette)

    #Added a zoom projection_scale
    fig.update_layout(
        geo = dict(
            projection_scale=2.7, #Zoom
            center=dict(lat=40.0, lon=-58.0), #Center Point
        ))


    fig.update_geos(lataxis_showgrid=True, lonaxis_showgrid=True)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return fig