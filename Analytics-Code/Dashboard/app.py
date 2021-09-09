#!/usr/bin/env python3

# Author - Manoj Kesavulu

import dash
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from dash import html
import dash.html.Div as Div
from plotly.subplots import make_subplots
from dash.dependencies import Output, Input


data_10_frequency_timespent = pd.read_csv("../Insights/Metrics-10-frequency-timespent.csv")
data_11_frequency_timespent = pd.read_csv("../Insights/Metrics-11-frequency-timespent.csv")
data_consistency = pd.read_csv("../Insights/Metrics-consistency.csv")


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Usage Analytics Dashboard"


app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(children="Usage Analytics Dashboard", className="header-title"),
                html.P(children="Dashboard to visualise the usage analytics results of the Odoo application between versions 10 and 11", className="header-description")
            ]
        ),
        html.Div(
            children=[
                html.P(children="Select an User ID to view the results", className="menu-title-center"),
                dcc.Dropdown(
                    id='userId_value',
                    options=[
                        #{'label': 'All', 'value': '0'},
                        {'label': i, 'value': i} for i in data_10_frequency_timespent.userId.unique()
                    ],
                    placeholder="Default = All users",
                    className="menu"
                    ),    
                dcc.Graph(id="frequency-graph"),
                dcc.Graph(id="timespent-graph"),
                dcc.Graph(id="consistency-frequency-graph"),
                dcc.Graph(id="consistency-timespent-graph")
            ]
        )
    ]
)


@app.callback(
    [Output("frequency-graph", "figure"), 
    Output("timespent-graph", "figure"),
    Output("consistency-frequency-graph", "figure"),
    Output("consistency-timespent-graph", "figure")],
    [Input("userId_value", "value")])
def display_(userId_value):
    if userId_value == None:
        df_10_ft = data_10_frequency_timespent
        df_11_ft = data_11_frequency_timespent
    else:
        df_10_ft = data_10_frequency_timespent[data_10_frequency_timespent["userId"]==userId_value]
        df_11_ft = data_11_frequency_timespent[data_11_frequency_timespent["userId"]==userId_value]
    
    trace_frequency_10 = go.Bar(
        x = df_10_ft.actionName,
        y = df_10_ft.frequency,
        name = "Odoo 10",
        marker = dict(color = 'rgba(0, 190, 224, 0.95)',
                     line=dict(color='rgb(0,0,0)',width=1.5)),
        text = data_10_frequency_timespent.frequency)
    # create trace_frequency_11 
    trace_frequency_11 = go.Bar(
        x = df_11_ft.actionName,
        y = df_11_ft.frequency,
        name = "Odoo 11",
        marker = dict(color = 'rgba(252, 69, 53, 0.95)',
                      line=dict(color='rgb(0,0,0)',width=1.5)),
        text = data_11_frequency_timespent.frequency)

    data_frequency = [trace_frequency_10, trace_frequency_11]
    layout_frequency = go.Layout(barmode = "group", height=600, title="Frequency")
    fig_frequency = go.Figure(data = data_frequency, layout = layout_frequency)


    trace_timespent_10 = go.Bar(
        x = df_10_ft.actionName,
        y = df_10_ft.timespent,
        name = "Odoo 10",
        marker = dict(color = 'rgba(255, 167, 5, 0.95)',
                     line=dict(color='rgb(0,0,0)',width=1.5)),
        text = data_10_frequency_timespent.timespent)

    trace_timespent_11 = go.Bar(
        x = df_11_ft.actionName,
        y = df_11_ft.timespent,
        name = "Odoo 11",
        marker = dict(color = 'rgba(0, 204, 132, 0.95)',
                     line=dict(color='rgb(0,0,0)',width=1.5)),
        text = data_11_frequency_timespent.timespent)
    
    data_timespent = [trace_timespent_10, trace_timespent_11]
    layout_timespent = go.Layout(barmode = "group", height=600, title="Time Spent")
    fig_timespent = go.Figure(data = data_timespent, layout = layout_timespent)

    
    # Plot figures for Consistency measures 
    fig_consistency_frequency = px.histogram(
        data_consistency, 
        x="actionName", 
        y="consistency_frequency", 
        color="userId",
        marginal="box", 
        height=900, 
        title="Consistency of Frequency")
    
    fig_consistency_timespent = px.histogram(
        data_consistency, 
        x="actionName", 
        y="consistency_timespent", 
        color="userId",
        marginal="box", 
        height=900, 
        title="Consistency of Time Spent")
    #iplot(fig)
    return fig_frequency, fig_timespent, fig_consistency_frequency, fig_consistency_timespent


if __name__ == "__main__":
    app.run_server(debug=True)