import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html, dcc, Input, Output

dash.register_page(__name__, path="/data-analysis")

# Load and prepare data
df = pd.read_csv("data/airline_dec_2008_50k.csv", index_col=0, low_memory=False)
delay_cols = ['CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay']
df['DepHour'] = pd.to_numeric(df['DepTime'], errors='coerce') // 100
df['Route'] = df['Origin'] + " → " + df['Dest']

route_delays = df.groupby(['Origin', 'Dest'])['ArrDelay'].mean().reset_index()
route_delays = route_delays.sort_values(by='ArrDelay', ascending=False).dropna().head(20)
labels = pd.concat([route_delays['Origin'], route_delays['Dest']]).unique().tolist()
label_idx = {airport: i for i, airport in enumerate(labels)}
route_delays['source'] = route_delays['Origin'].map(label_idx)
route_delays['target'] = route_delays['Dest'].map(label_idx)


# Delays' tab
delay_dropdown = dcc.Dropdown(
    options=[{"label": col, "value": col} for col in delay_cols],
    value="CarrierDelay",
    id="delay-type-dropdown-analysis"
)

delay_distribution_graph = dcc.Graph(id="delay-distribution-analysis")

fig_daily_delay = px.line(
    df.groupby('DayofMonth')['ArrDelay'].mean().reset_index(),
    x='DayofMonth', y='ArrDelay', markers=True,
    title='📈 Daily Average Arrival Delay',
    labels={'DayofMonth': 'Day', 'ArrDelay': 'Avg Delay (min)'}
)

fig_delay_hour = px.line(
    df.groupby('DepHour')['DepDelay'].mean().reset_index(),
    x='DepHour', y='DepDelay', markers=True,
    title='⏰ Avg Departure Delay by Hour',
    labels={'DepHour': 'Hour', 'DepDelay': 'Avg Departure Delay (min)'}
)
delays_tab = dcc.Tab(label="Delays", children=[
    html.Br(),
    html.Label("Select Delay Type:"),
    delay_dropdown,
    delay_distribution_graph,

    # Daily Average Arrival Delay
    dcc.Graph(figure=fig_daily_delay),

    # Avg Departure Delay by Hour
    dcc.Graph(figure=fig_delay_hour),

    # Arrival Delay by Flight Distance
    dcc.Graph(figure=px.box(
        df.assign(DistanceBin=pd.cut(df['Distance'], bins=[0, 250, 500, 1000, 1500, 2000, 3000],
                                     labels=['<250mi', '250-500mi', '500-1000mi', '1k-1.5k', '1.5k-2k', '2k-3k'])),
        x='DistanceBin', y='ArrDelay',
        title='📦 Arrival Delays by Flight Distance',
        labels={'ArrDelay': 'Arrival Delay (min)', 'DistanceBin': 'Distance Range'}
    )),

    # Average Delay by Carrier
    dcc.Graph(figure=px.bar(
        df.groupby('UniqueCarrier')['ArrDelay'].mean().sort_values().reset_index(),
        x='UniqueCarrier', y='ArrDelay',
        title='📊 Average Arrival Delay by Airline',
        labels={'ArrDelay': 'Average Delay (minutes)', 'UniqueCarrier': 'Airline'},
        color='ArrDelay', color_continuous_scale='RdBu'
    )),

    dcc.Graph(
        figure=px.scatter(
            df, x='TaxiOut', y='DepDelay',
            title='🚕 Taxi-Out Time vs Departure Delay',
            labels={'TaxiOut': 'Taxi-Out Time (min)', 'DepDelay': 'Departure Delay (min)'},
            trendline='ols',
            opacity=0.6
        )
    ),

    dcc.Graph(
        figure=go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels,
            ),
            link=dict(
                source=route_delays['source'],
                target=route_delays['target'],
                value=route_delays['ArrDelay'],
                hovertemplate='Route: %{source.label} → %{target.label}<br>Avg Delay: %{value:.1f} min<extra></extra>',
            )
        )]).update_layout(title_text="✈️ Top 20 Most Delayed Routes", font_size=12)
    )

])


# Cancellations' tab
cancel_data = df.groupby("UniqueCarrier")["Cancelled"].sum().sort_values().reset_index()
fig_cancel = px.bar(cancel_data,
    x="UniqueCarrier", y="Cancelled",
    title="🚫 Cancellations by Airline",
    labels={"UniqueCarrier": "Airline", "Cancelled": "Total Cancellations"},
    color="Cancelled", color_continuous_scale="Reds"
)

cancellation_tab = dcc.Tab(label="Cancellations", children=[
    html.Br(),
    dcc.Graph(figure=fig_cancel)
])

# Routes' tab
top_routes = df['Route'].value_counts().head(10).sort_values(ascending=True).reset_index()
top_routes.columns = ['Route', 'Count']
fig_routes = px.bar(
    top_routes,
    x='Count', y='Route',
    orientation='h',
    title='🛫 Top 10 Busiest Flight Routes',
    labels={'Count': 'Number of Flights', 'Route': 'Route'},
    color='Count', color_continuous_scale='Blues'
)

routes_tab = dcc.Tab(label="Routes", children=[
    html.Br(),
    dcc.Graph(figure=fig_routes)
])

# Flight Trends' tab
day_map = {1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat", 7: "Sun"}
day_freq = df['DayOfWeek'].map(day_map).value_counts().reindex(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
fig_dow = px.bar(
    x=day_freq.index, y=day_freq.values,
    labels={"x": "Day of Week", "y": "Number of Flights"},
    title="📆 Flights by Day of Week"
)

hourly_counts = (
    df.groupby(['DayofMonth', 'DepHour']).size().reset_index(name='FlightCount')
    .groupby('DepHour')['FlightCount'].mean().reset_index()
)
fig_hour = px.line(
    hourly_counts, x='DepHour', y='FlightCount', markers=True,
    title='🕑 Avg Flights Per Hour Per Day',
    labels={'DepHour': 'Hour of Day', 'FlightCount': 'Avg Flights'}
)

flight_trends_tab = dcc.Tab(label="Flight Trends", children=[
    html.Br(),
    dcc.Graph(figure=fig_dow),
    dcc.Graph(figure=fig_hour)
])

# Final Layout
layout = dbc.Container([
    html.H2("📊 Flight Data Analysis"),
    dcc.Tabs([
        delays_tab,
        cancellation_tab,
        routes_tab,
        flight_trends_tab
    ])
], fluid=True)


@dash.callback(
    Output("delay-distribution-analysis", "figure"),
    Input("delay-type-dropdown-analysis", "value")
)
def update_delay_distribution(colname):
    fig = px.histogram(
        df, x=colname, nbins=50,
        title=f"{colname} Distribution",
        labels={colname: "Delay (min)"}
    )
    fig.update_layout(yaxis_title="Flight Count")
    return fig
