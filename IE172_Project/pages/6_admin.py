import dash
from dash import dcc, html

dash.register_page(__name__, name="Admin Dashboard")

layout = html.Div(
    [
        # Add a header for the Admin Dashboard page
        html.H1(
            "Admin Dashboard", 
            className="text-light fw-bold fs-1 text-center", 
            style={'margin-bottom': '20px'}
        ),

        # Section for adding, updating, and deleting movies, customers, employees, and showtimes
        html.P(
            "<add, update, and delete movies, customers, employees, and showtimes>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),

        # Section for financial records
        html.P(
            "<financial records>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),

        # Section for employee management
        html.P(
            "<employee management>",
            className="text-light fw-bold fs-3",
            style={'textAlign': 'center', 'margin-bottom': '20px'}
        ),
    ]
)
