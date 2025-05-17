import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html

dash.register_page(__name__, path="/")

df = pd.read_csv("data/airline_dec_2008_50k.csv", index_col=0, low_memory=False)

fig_delay_dist = px.histogram(df, x="ArrDelay", nbins=60, title="Arrival Delay Distribution")
fig_by_day = px.histogram(df, x="DayOfWeek", title="Flights by Day of Week")
fig_by_carrier = px.bar(df.groupby("UniqueCarrier")["ArrDelay"].mean().reset_index(),
                        x="UniqueCarrier", y="ArrDelay", title="Average Delay by Carrier")

layout = dbc.Container([
    html.H2("Flights Dataset Description"),
    html.Hr(),

    html.Div([
        html.P(f"The dataset contains {df.shape[0]} rows and {df.shape[1]} columns. The descriptions of these features were referenced from the Bureau of Transportation Statistics (BTS) as they were not included in Kaggle."),
        dbc.Table([
            html.Thead(html.Tr([html.Th("Feature"), html.Th("Description")])),
            html.Tbody([
                html.Tr([html.Td("Year"), html.Td("The year when the flight took place.")]),
                html.Tr([html.Td("Month"), html.Td("The month (1–12) when the flight took place.")]),
                html.Tr([html.Td("DayOfMonth"), html.Td("The day of the month (1–31) when the flight took place.")]),
                html.Tr([html.Td("DayOfWeek"), html.Td("The day of the week (1–7, Monday to Sunday).")]),
                html.Tr([html.Td("DepTime"), html.Td("Actual departure time.")]),
                html.Tr([html.Td("CRSDepTime"), html.Td("Scheduled departure time (Computerized Reservation System).")]),
                html.Tr([html.Td("ArrTime"), html.Td("Actual arrival time.")]),
                html.Tr([html.Td("CRSArrTime"), html.Td("Scheduled arrival time (CRS).")]),
                html.Tr([html.Td("UniqueCarrier"), html.Td("Unique carrier code.")]),
                html.Tr([html.Td("FlightNum"), html.Td("Flight number.")]),
                html.Tr([html.Td("TailNum"), html.Td("Aircraft tail number.")]),
                html.Tr([html.Td("ActualElapsedTime"), html.Td("Actual flight duration in minutes.")]),
                html.Tr([html.Td("CRSElapsedTime"), html.Td("Scheduled flight duration in minutes.")]),
                html.Tr([html.Td("AirTime"), html.Td("Time in the air in minutes.")]),
                html.Tr([html.Td("ArrDelay"), html.Td("Arrival delay in minutes (positive = late, negative = early).")]),
                html.Tr([html.Td("DepDelay"), html.Td("Departure delay in minutes.")]),
                html.Tr([html.Td("Origin"), html.Td("Origin airport code.")]),
                html.Tr([html.Td("Dest"), html.Td("Destination airport code.")]),
                html.Tr([html.Td("Distance"), html.Td("Flight distance in miles.")]),
                html.Tr([html.Td("TaxiIn"), html.Td("Taxi-in time (landing to gate).")]),
                html.Tr([html.Td("TaxiOut"), html.Td("Taxi-out time (gate to takeoff).")]),
                html.Tr([html.Td("Cancelled"), html.Td("1 = cancelled, 0 = not cancelled.")]),
                html.Tr([html.Td("CancellationCode"), html.Td("Reason: A = Carrier, B = Weather, C = NAS, D = Security.")]),
                html.Tr([html.Td("Diverted"), html.Td("1 = flight diverted, 0 = not diverted.")]),
                html.Tr([html.Td("CarrierDelay"), html.Td("Minutes delayed due to the carrier.")]),
                html.Tr([html.Td("WeatherDelay"), html.Td("Minutes delayed due to weather.")]),
                html.Tr([html.Td("NASDelay"), html.Td("Minutes delayed due to National Air System.")]),
                html.Tr([html.Td("SecurityDelay"), html.Td("Minutes delayed due to security.")]),
                html.Tr([html.Td("LateAircraftDelay"), html.Td("Minutes delayed due to late arrival of aircraft.")])
            ])
        ], bordered=True, hover=True, responsive=True, striped=True),
    ], className="mb-4"),

    html.Div([
            html.H4("Dataset Preview: First 5 Rows"),
            dbc.Table.from_dataframe(df.head(), striped=True, bordered=True, hover=True)
        ], className="mb-4"),

    html.Div([
            html.H4("Missing Values Overview"),
            html.Img(src="/assets/missing_matrix.png",style={"width": "100%"})
        ], className="mb-4"),

    html.Div([
        html.H4("Dataset Summary Statistics (Numerical Columns)"),
        dbc.Table.from_dataframe(
            df.describe().T.round(2).reset_index().rename(columns={"index": "Feature"}),
            striped=True,
            bordered=True,
            hover=True
        )

    ], className="mb-4"),


], fluid=True)
