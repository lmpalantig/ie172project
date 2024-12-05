import dash
from dash import dcc, html

dash.register_page(__name__, name="Ticketing")

layout = html.Div(
    [
        # Add a header for the Ticketing page
        html.H1(
            "Movie Ticketing and Schedule", 
            className="text-light fw-bold fs-1 text-center", 
            style={'margin-bottom': '20px'}
        ),

        # Movie schedule section
        html.P(
            "<movie schedule>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),

        # Purchase form section
        html.P(
            "<purchase form>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),
    ]
)
