import pandas as pd
import streamlit as st
import zipfile
from streamlit_folium import st_folium
"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


import driftmlp
import functools
def get_network(_str_append):
    network = driftmlp.network_from_file('transition_'+_str_append+'.GraphML', visual=False)
    return network
EXP_STR =(
    """
    Blue lines are going from the blue point to the red point above.
    Red lines are going from the red point to the blue point above.
    """)
class interactive_app:
    def __init__(self):
        self.network = None
        self.network_type = None
        self.__name__ = 'interactive_app'

    def __call__(self, lon_from, lat_from, lon_to, lat_to, network_type):
        ### This is relatively expensive so only do it when needed
        if network_type != self.network_type or self.network is None:
            self.network = get_network(network_type)
            self.network_type = network_type

        from_loc = (lon_from, lat_from)
        to_loc = (lon_to, lat_to)
        path = driftmlp.shortest_path.SingleSP(self.network, from_loc, to_loc)
        if path.sp.travel_time != -1:
            m = path.plot_folium()
            #print(EXP_STR)
            #display(path)
            return m
        else:
            return
            #print("No Path Found")
graph_zip = zipfile.ZipFile("graph_files.zip")
graph_zip.extractall()

app = interactive_app()
st.cache(app)
with st.echo(code_location='below'):


    p = st.radio(
        label = "Drogued",
        options=['No Drogued Drifters', 'Drogued Drifters', 'Both Drogued and Undrogued'],
    )
    options_map = {"No Drogued Drifters": "nodrg",
                    "Drogued Drifters": "drg",
                    "Both Drogued and Undrogued": "both"}
    lon_from=st.slider(label ="lon_from", value=-158.0, min_value=-180.0, max_value=180.0)
    lat_from = st.slider(label = "lat_from", value=44.0, min_value=-80.0, max_value=80.0)
    lon_to = st.slider(label ="lon_to", value=-19.55, min_value=-180.0, max_value=180.0)
    lat_to = st.slider(label = "lat_to", value=-52.0, min_value=-80.0, max_value=80.0)

    map = app(lon_from=lon_from, lat_from=lat_from, lat_to=lat_to, lon_to=lon_to, network_type=options_map[p])
    st_folium(map, width=700, height=900)
