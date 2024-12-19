import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc
from dash import dash_table
import pandas as pd
import plotly.express as px
import dbconnect as db

# Register the page
dash.register_page(__name__, name='Updates', path='/updates')

# Query to fetch data
data_query = """
    SELECT 
        producer_id AS ID, 
        producer_name AS "Producer Name", 
        producer_address AS Address, 
        producer_contact_information AS "Contact Information", 
        producer_current_balance AS "Current Balance"
    FROM Producer
"""
df_columns = ["ID", "Producer Name", "Address", "Contact Information", "Current Balance"]

# Initial Data Fetch
def fetch_data():
    try:
        return db.getDataFromDB(data_query, None, df_columns)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame(columns=df_columns)

# Layout components
producers_tab = html.Div(
    [
        dbc.Row(
            [
                # Left section: Form to add a new producer
                dbc.Col(
                    [
                        html.H4("Add New Producer Information", className='mb-4 text-left'),
                        dbc.Form(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Producer Name"), width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                id="producer-name", 
                                                placeholder="Enter producer name"
                                            ),
                                            width=8,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Address"), width=4),
                                        dbc.Col(
                                            dbc.Textarea(
                                                id="producer-address", 
                                                placeholder="Enter producer address"
                                            ),
                                            width=8,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Contact Information"), width=4),
                                        dbc.Col(
                                            dbc.Textarea(
                                                id="producer-contact", 
                                                placeholder="Enter producer contact information"
                                            ),
                                            width=8,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dbc.Label("Current Balance"), width=4),
                                        dbc.Col(
                                            dbc.Input(
                                                id="producer-balance", 
                                                type="number", 
                                                placeholder="Enter current balance"
                                            ),
                                            width=8,
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                # Center-align the button and message
                                html.Div(
                                    dbc.Button(
                                        "Add Producer", 
                                        id="add-producer-btn", 
                                        color="primary", 
                                        className="mt-3"
                                    ),
                                    className="text-center",
                                ),
                                html.Div(
                                    id="add-producer-message", 
                                    className="mt-3 text-center",
                                ),
                            ]
                        ),
                    ],
                    className="bg-dark rounded-3 p-4",
                ),

                # Right section: Graph of the data
                dbc.Col(
                    [
                        html.H4("Data Graph", className='mb-4'),
                        dcc.Graph(id="producer-graph"),
                    ],
                    className="bg-dark rounded-3 p-4",
                    width=5,
                ),
            ],
           className="gap-3 p-3",
        ),
        # Bottom section: Data table
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Data Table", className='mb-2'),
                        dash_table.DataTable(
                            id="producer-table",
                            columns=[{"name": col, "id": col} for col in df_columns],
                            style_table={'border': '1px solid grey', "borderRadius": "5px", 'overflow': 'hidden'},
                            style_as_list_view=True,
                            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white', 'fontWeight': 'bold', 'border': 'none'},
                            style_data={'backgroundColor': 'rgb(50, 50, 50)','color': 'white'},
                            style_cell={'textAlign': 'left', 'font-family': 'Calibri', 'border': '1px solid grey','paddingLeft': '5px'},
                            style_cell_conditional=[
                                {'if': {'column_id': 'ID'}, 'width': '5%'},
                                {'if': {'column_id': 'Producer Name'}, 'width': '20%'},
                                {'if': {'column_id': 'Address'}, 'width': '30%'},
                                {'if': {'column_id': 'Contact Information'},'width': '30%'},
                                {'if': {'column_id': 'Current Balance'}, 'textAlign': 'right', 'paddingRight': '5px'},
                            ],
                            row_deletable=True,
                        ),
                    ],
                ),
            ],
            className="bg-dark rounded-3 mx-1 mb-3 p-3"
        ),
    ]
)

# Tabs for layout
tabs = dbc.Tabs(
    [
        dbc.Tab(producers_tab, label="Producers"),
    ]
)

# Page layout
layout = dbc.Container(
    [
        tabs,
    ],
)

# Callbacks for interactivity
@callback(
    Output("add-producer-message", "children"),
    Output("producer-table", "data"),
    Output("producer-graph", "figure"),
    Output("producer-name", "value"),
    Output("producer-address", "value"),
    Output("producer-contact", "value"),
    Output("producer-balance", "value"),
    Input("add-producer-btn", "n_clicks"),
    Input("producer-table", "data_previous"),
    State("producer-table", "data"),
    State("producer-name", "value"),
    State("producer-address", "value"),
    State("producer-contact", "value"),
    State("producer-balance", "value"),
)
def manage_producers(n_clicks, data_previous, current_data, producer_name, producer_address, producer_contact, producer_balance):
    # Handle initial data load
    if n_clicks is None and data_previous is None:
        producers_data = fetch_data()
        fig = px.bar(
            producers_data, 
            x="Producer Name", 
            y="Current Balance", 
            height=350
        )
        # Apply dark mode styling to the figure
        fig.update_layout(
            plot_bgcolor="rgb(30,30,30)",
            paper_bgcolor="rgb(30,30,30)",
            font=dict(color="white"),
            xaxis=dict(showgrid=False, color="white"),
            yaxis=dict(showgrid=True, gridcolor="rgb(50,50,50)", color="white"),
        )
        return "", producers_data.to_dict("records"), fig, None, None, None, None

    # Handle row deletions
    if data_previous is not None and data_previous != current_data:
        deleted_rows = [row for row in data_previous if row not in current_data]
        for row in deleted_rows:
            try:
                db.modifyDB("DELETE FROM Producer WHERE producer_id = %s", (row["ID"],))
            except Exception as e:
                return f"Error deleting row: {e}", current_data, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # Validate new producer data
    if not producer_name or not producer_address or not producer_contact or producer_balance is None:
        producers_data = fetch_data()
        fig = px.bar(
            producers_data, 
            x="Producer Name", 
            y="Current Balance", 
            height=350
        )
        # Apply dark mode styling to the figure
        fig.update_layout(
            plot_bgcolor="rgb(30,30,30)",
            paper_bgcolor="rgb(30,30,30)",
            font=dict(color="white"),
            xaxis=dict(showgrid=False, color="white"),
            yaxis=dict(showgrid=True, gridcolor="rgb(50,50,50)", color="white"),
        )
        return (
            "Error: Please fill in all fields.",
            producers_data.to_dict("records"),
            fig,
            producer_name, producer_address, producer_contact, producer_balance
        )

    # Add a new producer
    if n_clicks:
        sql = """
            INSERT INTO Producer (
                producer_name, 
                producer_address, 
                producer_contact_information, 
                producer_current_balance
            ) VALUES (%s, %s, %s, %s)
        """
        values = (producer_name, producer_address, producer_contact, producer_balance)
        try:
            db.modifyDB(sql, values)
            message = "Producer added successfully!"
        except Exception as e:
            message = f"Error: {e}"
        producers_data = fetch_data()
        fig = px.bar(
            producers_data, 
            x="Producer Name", 
            y="Current Balance", 
            height=350,
        )
        # Apply dark mode styling to the figure
        fig.update_layout(
            plot_bgcolor="rgb(30,30,30)",
            paper_bgcolor="rgb(30,30,30)",
            font=dict(color="white"),
            xaxis=dict(showgrid=False, color="white"),
            yaxis=dict(showgrid=True, gridcolor="rgb(50,50,50)", color="white"),
        )
        return message, producers_data.to_dict("records"), fig, None, None, None, None

    # Fetch updated data for any other state
    producers_data = fetch_data()
    fig = px.bar(
        producers_data, 
        x="Producer Name", 
        y="Current Balance", 
        height=350,
    )
    # Apply dark mode styling to the figure
    fig.update_layout(
        plot_bgcolor="rgb(30,30,30)",
        paper_bgcolor="rgb(30,30,30)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False, color="white"),
        yaxis=dict(showgrid=True, gridcolor="rgb(50,50,50)", color="white"),
    )
    return "", producers_data.to_dict("records"), fig, None, None, None, None
