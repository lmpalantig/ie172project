import dash
from dash import dcc, html

dash.register_page(__name__, name="Reports")

layout = html.Div(
    [
        # Add a header for the Reports page
        html.H1(
            "Reports Overview", 
            className="text-light fw-bold fs-1 text-center", 
            style={'margin-bottom': '20px'}
        ),

        # Section for top movies
        html.P(
            "<top movies>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),

        # Section for ticket sales analysis
        html.P(
            "<ticket sales analysis>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),

        # Section for graphs and charts
        html.P(
            "<graphs and charts>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),
    ]
)
