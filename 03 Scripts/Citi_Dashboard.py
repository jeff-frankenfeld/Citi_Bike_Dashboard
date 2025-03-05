################################################ CITI BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt

########################### Initial settings for the dashboard ##################################################################

st.set_page_config(page_title="Citi Bike Strategy Dashboard", layout="wide")

# Dashboard Title
st.title("Citi Bike Strategy Dashboard")

# Dashboard Introduction
st.markdown(
    "This dashboard analyzes Citi Bike usage patterns and availability issues across NYC. "
    "By identifying the root causes of distribution challenges, we aim to provide data-driven solutions "
    "to optimize bike placement and ensure better accessibility for riders."
)

########################## Import data ###########################################################################################

import os

@st.cache_data
def load_data():
    # Define absolute paths for local use
    file_path_df = r"C:\Users\HP\Citi_Bike_Dashboard\02 Data\Prepared Data\reduced_data_to_plot_2.6.csv"
    file_path_top20 = r"C:\Users\HP\Citi_Bike_Dashboard\02 Data\Prepared Data\top20.csv"

    # Load datasets
    df = pd.read_csv(file_path_df, index_col=0)
    top20 = pd.read_csv(file_path_top20, index_col=0)

    # Reduce memory usage
    df[['bike_rides_daily', 'avgTemp']] = df[['bike_rides_daily', 'avgTemp']].astype('float32')
    
    return df, top20

df, top20 = load_data()  # Uses cached data for better performance

# Reduce data size before sending to the browser
df_downsampled = df.iloc[::20, :]  # Keep every 20th row (best for time-series analysis)

########################################## DEFINE THE CHARTS #####################################################################

## Bar Chart

# Create a bar chart with layout settings in one block
fig = go.Figure(
    data=[
        go.Bar(
            x=top20['start_station_name'],  # X-axis: Station names
            y=top20['value'],  # Y-axis: Number of trips
            marker={'color': top20['value'], 'colorscale': 'Blues'}  # Apply color scale
        )
    ],
    layout=go.Layout(
        title="Top 20 most popular bike stations in New York City",  # Chart title
        xaxis=dict(
            title=dict(
                text="Start Stations",  # X-axis title
                standoff=20  # Adds space between x-axis title and tick labels
            ),
            tickangle=-45  # Rotates x-axis labels to avoid overlap
        ),
        yaxis=dict(title="Sum of trips"),  # Y-axis title
        width=900,
        height=600
    )
)

# Display the bar chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

## Line Chart

# Create a figure with a secondary Y-axis
fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

# Add first trace: Line chart for daily bike rides (Primary Y-axis)
fig_2.add_trace(
    go.Scatter(
        x=df_downsampled['date'],  # X-axis: Date
        y=df_downsampled['bike_rides_daily'],  # Y-axis: Number of bike rides
        name='Daily bike rides',  # Legend label
        marker={'color': 'blue'}, # Apply color scale 
    ),
    secondary_y=False  # Assign to primary Y-axis
)

# Add second trace: Line chart for daily temperature (Secondary Y-axis)
fig_2.add_trace(
    go.Scatter(
        x=df_downsampled['date'],  # X-axis: Date
        y=df_downsampled['avgTemp'],  # Y-axis: Average daily temperature
        name='Daily temperature',  # Legend label
        marker={'color': df['avgTemp'],'color': 'red'}, # Apply color scale
    ),
    secondary_y=True  # Assign to secondary Y-axis
)

fig_2.update_layout(
    title = 'Daily bike trips and temperatures in 2022',
    height = 600
)

# Display the line chart in Streamlit
st.plotly_chart(fig_2, use_container_width=True)

### Add the map ###

# Define absolute file path for local execution
path_to_html = r"C:\Users\HP\Citi_Bike_Dashboard\04 Analysis\Visualizations\Citi_Bike_Trips_Aggregated.html"

# Read file and store in variable
with open(path_to_html, 'r', encoding='utf-8') as f:  
    html_data = f.read()

# Display the map in Streamlit
st.subheader("Aggregated Bike Trips in New York City")
st.components.v1.html(html_data, height=1000)
