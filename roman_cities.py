# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:11:08 2022

@author: Utilizador
"""

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output



app = Dash(__name__)

# -- Import and clean data (importing xlsx into pandas)
df = pd.read_excel("data/Hanson2016_CitiesDatabase_OxREP.xlsx", sheet_name="Cities")


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(children=[ 
    html.H1("Ancient roman world", style={'text-align': 'center', 'color': '#FA5835'}),

    dcc.Slider(id='slider', 
               min=df["Start Date"].min(), 
               max=df["Start Date"].max(), 
               step=25, value=-300,
               marks={-900: "900 BC",
                      -500: "500 BC",
                      1: "1 AD",
                      200: "200 AD"},
               tooltip={"placement": "bottom", "always_visible": True}),
    
    html.Br(),

    html.Div(id='title', children=[], style={'text-align': 'center', 'color': '#FA5835'}),
    html.Br(),

    dcc.Graph(id='map', figure={})

])


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='title', component_property='children'),
     Output(component_id='map', component_property='figure')],
    [Input(component_id='slider', component_property='value'),]
)
def update_graph(value):

    if value < 0 :
        display_year = str(abs(value)) + " BC"
    else:
        display_year = str(abs(value)) + " AD"
    container = "Roman cities by {}".format(display_year)

    dff = df.copy()
    dff = dff.loc[dff["Start Date"] <= value]

    # Plotly Express
    fig = px.scatter_mapbox(
        dff, 
        lat="Latitude (Y)", 
        lon="Longitude (X)", 
        hover_name="Ancient Toponym", 
        hover_data=["Modern Toponym", "Start Date"],
        color_discrete_sequence=["#FA5835"], 
        zoom=3, 
        height=400,
        opacity=0.7,
        template='plotly_dark',)

    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)