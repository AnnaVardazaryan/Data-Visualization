import dash
import dash_bootstrap_components as dbc
from dash import dcc

app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.FLATLY]
)

server = app.server

app.layout = dbc.Container([
    dbc.NavbarSimple(
        brand="Flight Data Dashboard",
        color="primary",
        dark=True,
        children=[
            dbc.NavItem(dcc.Link("Overview", href="/", className="nav-link")),
            dbc.NavItem(dcc.Link("Data Analysis", href="/data-analysis", className="nav-link")),
            dbc.NavItem(dcc.Link("Geographic View", href="/geo-plot", className="nav-link"))
        ]
    ),
    dash.page_container
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)
