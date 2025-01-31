import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.title = 'AI Passport Interactive Tutorial'

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavLink("Landscape of Biomedical Engineering", href="/lbs", active="exact"),
            dbc.NavLink("Traditional Biomedical Analysis", href="/tba", active="exact"),
        ],
        brand="AI Passport",
        color="primary",
        dark=True,
    ),
    dash.page_container
])

server = app.server
