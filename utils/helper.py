import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def display_map(data: pd.DataFrame, coords_to_highlight: tuple = None):
    
    fig = px.scatter_mapbox(
                            data, 
                            lat="Latitude (Y)", 
                            lon="Longitude (X)", 
                            hover_name="Ancient Toponym", 
                            hover_data=["Modern Toponym", "Start Date"],
                            color_discrete_sequence=["#FA5835"], 
                            zoom=3, 
                            height=400,
                            opacity=0.7,
                            template="plotly_dark",
                            )

    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    if coords_to_highlight:

        # Unpack coordinates:
        lat, lon = coords_to_highlight

        # Highlight point:
        fig.add_trace(go.Scattermapbox(lat=[lat],
                                       lon=[lon],
                                       mode="markers",
                                       marker=dict(size=15, color="yellow")
                                       )
                      )

    return fig



def convert_value_to_year(value: int):
    if value < 0 :
        return f"{abs(value)} BC"
    return f"{abs(value)} AD"  
    
    