# -*- coding: utf-8 -*-
"""
Created on Sat May 28 23:11:08 2022

@author: Utilizador
"""

import pandas as pd
from dash import Dash, dcc, html, Input, Output
from utils import helper


app = Dash(__name__)

# Import data:
df = pd.read_excel("data/Hanson2016_CitiesDatabase_OxREP.xlsx", sheet_name="Cities")


# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div(children=[ 
    html.H1("Ancient roman world", style={"text-align": "center", "color": "#FA5835"}),

    dcc.Slider(id="slider", 
               min=df["Start Date"].min(), 
               max=df["Start Date"].max(), 
               step=25, value=-300,
               marks={-900: "900 BC",
                      -500: "500 BC",
                      1: "1 AD",
                      200: "200 AD"},
               tooltip={"placement": "bottom", "always_visible": True}),
    
    html.Br(),

    html.Div(id="title", children=[], style={"text-align": "center", "color": "#FA5835"}),

    html.Br(),

    dcc.Graph(id="map", figure={}),

    html.Br(),

    html.Iframe(id="click-map", 
                src="", 
                style={"width": "100%", "height": "600px", "border": "none"}),

],
    style={"backgroundColor": "#000000"} 
)


# ------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output("title", "children"),
     Output("click-map", "src"), 
     Output("map", "figure")],
    [Input("map", "clickData"),
     Input("slider", "value")]
)
def update_graph_and_click(clickData, value):

    # Text to be displayed above the map:
    year = helper.convert_value_to_year(value)
    container = f"Roman cities by {year}"

    # Filter data:
    dff = df.copy()
    dff = dff.loc[dff["Start Date"] <= value]

    # Map:
    fig = helper.display_map(dff, coords_to_highlight=None)

    # Highlight point:
    if clickData is not None:
        clicked_point = clickData["points"][0]
        city_name = clicked_point["hovertext"]
        lat = clicked_point["lat"]
        lon = clicked_point["lon"]
    
        fig = helper.display_map(dff, coords_to_highlight=(lat, lon))
        wiki_url = f"https://en.wikipedia.org/wiki/{city_name}"
        return container, wiki_url, fig

    fig = helper.display_map(dff, coords_to_highlight=None)
    wiki_url = "https://en.wikipedia.org/wiki/Ancient_Rome"
    return container, wiki_url, fig
    


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    app.run_server(debug=True)