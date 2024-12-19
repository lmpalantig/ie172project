import dash
from dash import dcc, html

dash.register_page(__name__, name='Movies')

# Movie data
movies = [
    {
        "title": "Top Gun: Maverick",
        "showroom": "#1",
        "showtimes": ["10:00 AM", "2:00 PM", "6:00 PM"],
        "duration": "2h 11m",
        "capacity": 250,
        "image_url": "https://via.placeholder.com/150?text=Top+Gun+Maverick"  # Replace with actual movie poster URL
    },
    {
        "title": "Oppenheimer",
        "showroom": "#2",
        "showtimes": ["9:00 AM", "1:30 PM", "6:00 PM"],
        "duration": "3h",
        "capacity": 250,
        "image_url": "https://via.placeholder.com/150?text=Oppenheimer"  # Replace with actual movie poster URL
    },
    {
        "title": "Everything Everywhere All at Once",
        "showroom": "#3",
        "showtimes": ["11:00 AM", "3:00 PM", "7:30 PM"],
        "duration": "2h 20m",
        "capacity": 250,
        "image_url": "https://via.placeholder.com/150?text=Everything+Everywhere"  # Replace with actual movie poster URL
    },
    {
        "title": "The Batman",
        "showroom": "#4",
        "showtimes": ["10:30 AM", "3:00 PM", "8:00 PM"],
        "duration": "2h 56m",
        "capacity": 250,
        "image_url": "https://via.placeholder.com/150?text=The+Batman"  # Replace with actual movie poster URL
    },
]

# Layout
layout = html.Div(
    [
        # Header
        html.H1(
            "Now Showing",
            className="text-light fw-bold fs-1 text-center",
            style={'margin-bottom': '20px'}
        ),

        # Search bar and button
        html.Div(
            [
                dcc.Input(
                    id='movie-search',
                    type='text',
                    placeholder='Search for a movie...',
                    style={
                        'width': '80%',
                        'padding': '10px',
                        'borderRadius': '15px',
                        'border': '1px solid #ccc'
                    }
                ),
                html.Button(
                    'Search',
                    id='search-button',
                    n_clicks=0,
                    style={
                        'padding': '10px',
                        'margin-left': '10px',
                        'borderRadius': '15px',
                        'border': '1px solid #ccc'
                    }
                ),
            ],
            style={'display': 'flex', 'align-items': 'center', 'justify-content': 'center', 'padding': '10px'}
        ),

        # Movie cards
        html.Div(
            [
                html.Div(
                    className="movie-card",
                    children=[
                        html.Img(
                            src=movie["image_url"],
                            alt=f"{movie['title']} poster",
                            style={"width": "150px", "height": "225px", "margin-bottom": "10px"}
                        ),
                        html.H3(movie["title"], className="text-light"),
                        html.P(f"Showroom: {movie['showroom']}", className="text-light"),
                        html.P(f"Showtimes: {', '.join(movie['showtimes'])}", className="text-light"),
                        html.P(f"Duration: {movie['duration']}", className="text-light"),
                        html.P(f"Seats Available: {movie['capacity']} per showtime", className="text-light"),
                    ],
                    style={
                        "border": "1px solid #ccc",
                        "borderRadius": "10px",
                        "padding": "15px",
                        "margin": "10px",
                        "width": "200px",
                        "textAlign": "center",
                        "backgroundColor": "#2b2b2b",
                        "color": "white"
                    }
                )
                for movie in movies
            ],
            style={
                "display": "flex",
                "flexWrap": "wrap",
                "justifyContent": "center"
            }
        )
    ]
)
