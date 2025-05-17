import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

dash.register_page(__name__, path="/geo-plot")

df = pd.read_csv("data/airline_dec_2008_50k.csv", index_col=0)
airport_coords = pd.read_csv("data/airport_coords.csv")

# Count flights per origin and merge with coordinates
origin_counts = df['Origin'].value_counts().reset_index()
origin_counts.columns = ['IATA', 'Count']
merged = pd.merge(origin_counts, airport_coords, on="IATA", how="left").dropna(subset=['Latitude', 'Longitude'])

fig = go.Figure(go.Scattergeo(
    lon=merged['Longitude'],
    lat=merged['Latitude'],
    text=merged['IATA'] + "<br>Flights: " + merged['Count'].astype(str),
    mode='markers',
    marker=dict(
        size=merged['Count'] / merged['Count'].max() * 30,
        color=merged['Count'],
        colorscale='Blues',
        colorbar_title="Flights",
        line=dict(width=0.5, color='white')
    )
))

fig.update_layout(
    title_text="🗺️ Flight Origins in December 2008",
    geo=dict(scope='usa', projection_type='albers usa', showland=True),
    height=650
)

layout = dbc.Container([
    html.H2("Geographic View of Flight Routes"),
    html.P("This map displays the volume of flights departing from different US airports."),
    dcc.Graph(figure=fig)
], fluid=True)
