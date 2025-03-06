################################################ CITI BIKES DASHABOARD #####################################################

import streamlit as st
import pandas as pd
import numpy as np
import os
import requests
import zipfile
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static
from keplergl import KeplerGl
from datetime import datetime as dt
from numerize.numerize import numerize
from PIL import Image
from io import BytesIO

########################### Initial settings for the dashboard ####################################################


st.set_page_config(page_title = 'Citi Bike Strategy Dashboard', layout='wide')

# Dashboard Title
st.title("Citi Bike Strategy Dashboard")

# Define side bar
st.sidebar.title("Aspect Selector")
page = st.sidebar.selectbox('Select an aspect of the analysis',
  ["Intro Page","Weather Component and Bike Usage",
   "Most Popular Stations",
    "Interactive Map with Aggregated Bike Trips", "Trips by Hour: Weekday vs Weekend", "Conclusions and Recommendations"])

########################## Import data ###########################################################################################

@st.cache_data
def load_data():
        # URL of the ZIP file stored in GitHub (update with your actual username/repo)
        zip_url = "https://github.com/jeff-frankenfeld/Citi_Bike_Dashboard/raw/main/05%20Sent%20to%20Client/reduced_data_to_plot_7.zip"
    
        # Download the ZIP file from GitHub
        response = requests.get(zip_url)
        
        if response.status_code == 200:
            # Open the ZIP file
            with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_ref:
                # Extract the CSV file from the ZIP
                with zip_ref.open("reduced_data_to_plot_7.csv") as csv_file:
                    df = pd.read_csv(csv_file, index_col=0)
    
                    # Reduce memory usage
                    df[['bike_rides_daily', 'avgTemp']] = df[['bike_rides_daily', 'avgTemp']].astype('float32')
    
                    return df
        else:
            st.error("❌ Failed to load dataset. Please check the GitHub link.")
            return None  # Return None if the file couldn't be loaded
    
    df = load_data()
    
    if df is not None:
        df = df.reset_index()
        st.success("✅ Dataset successfully loaded!")
    else:
        st.error("❌ Dataset could not be loaded.")

######################################### DEFINE THE PAGES #####################################################################


### Intro page

if page == "Intro Page":

    st.markdown("""
    ### **Overview**
    Citi Bike is a vital part of NYC’s transportation system, but **bike availability issues** impact rider experience.  
    This dashboard **analyzes Citi Bike usage patterns** to uncover **key distribution challenges** and provide **data-driven solutions**.

    ### **What You’ll Find in This Dashboard**
    - **Weather & Bike Usage:** How temperature affects ridership.
    - **Most Popular Stations:** Where riders start their trips the most.
    - **Interactive Trip Map:** Key travel patterns across the city.
    - **Trips by Hour:** Comparing **weekday** vs. **weekend** rides.
    - **Conclusions & Recommendations:** **Optimized bike distribution strategies**.

    ### **How to Use This Dashboard**
    Use the **dropdown menu on the left** to navigate through the different insights.
    """)

    # URL of the image stored in GitHub (update with your actual username/repo)
    image_url = "https://raw.githubusercontent.com/jeff-frankenfeld/Citi_Bike_Dashboard/main/05%20Sent%20to%20Client/Citi_Bikes.jpg"
    
    # Download the image from GitHub
    response = requests.get(image_url)
    
    if response.status_code == 200:
        # Open the image
        intro_image = Image.open(BytesIO(response.content))
    
        # Display the image in Streamlit
        st.image(intro_image, use_column_width=True)
    else:
        st.error("❌ Failed to load intro image. Please check the GitHub link.")
    
### Create the dual axis line chart page ###

elif page == 'Weather Component and Bike Usage':

    fig_2 = make_subplots(specs=[[{"secondary_y": True}]])

    # Add first trace: Line chart for daily bike rides (Primary Y-axis)
    fig_2.add_trace(
    go.Scatter(
        x=df['date'],  # X-axis: Date
        y=df['bike_rides_daily'],  # Y-axis: Number of bike rides
        name='Daily bike rides',  # Legend label
        marker={'color': 'blue'}, # Apply color scale 
    ),
    secondary_y=False  # Assign to primary Y-axis
        )

    # Add second trace: Line chart for daily temperature (Secondary Y-axis)
    fig_2.add_trace(
    go.Scatter(
        x=df['date'],  # X-axis: Date
        y=df['avgTemp'],  # Y-axis: Average daily temperature
        name='Average Temperature (°C)',  # Legend label
        marker={'color': df['avgTemp'],'color': 'red'}, # Apply color scale
        ),
        secondary_y=True  # Assign to secondary Y-axis
    )

    fig_2.update_layout(
        title = 'Daily bike trips and temperatures in 2022',
        height = 400
        )

    # Display the line chart in Streamlit
    st.plotly_chart(fig_2, use_container_width=True)
    
    # Add in markdown comments
    st.markdown("""
    ### **Key Insights**
    - Bike ridership follows a seasonal pattern, peaking in warmer months and dropping in winter.
    - **Cold weather (below 10°C)** leads to a noticeable **decline in bike rides**.
    - **Warmer temperatures (above 15°C)** are associated with **higher ridership**, showing a clear correlation.

    ### **Next Step:**
    - Check out the **Conclusions and Recommendations** section to see how Citi Bike can optimize bike availability based on these insights.
    """)

### Most Popular Stations page ###

elif page == 'Most Popular Stations':

    # Sidebar filter to allow users to select one or multiple seasons for analysis
    with st.sidebar:
        season_filter = st.multiselect(
            label='Select the season', 
            options=df['season'].unique(),  # Get unique season values from the dataset
            default=df['season'].unique()   # Set all seasons as default selection
        )

    # Filter the dataframe based on the selected seasons
    # This keeps only the rows where the 'season' column matches the selected filters
    df1 = df[df['season'].isin(season_filter)].copy()  # Added .copy() to prevent warnings
    df1['value'] = 1

    # Define the total number of bike rides within the selected season(s)
    total_rides = float(df1['bike_rides_daily'].count())  

    # Display the total number of rides as a metric in the dashboard
    st.metric(label="Total Bike Rides", value=numerize(total_rides))

    # Group data by start station and aggregate trip counts
    df_groupby_bar = df1.groupby('start_station_name', as_index=False).agg({'value': 'sum'})

    # Select the top 20 stations with the highest trip counts
    top20 = df_groupby_bar.nlargest(20, 'value')

    # Create a bar chart visualization
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
                title="Start Stations",
                tickangle=-45,  # Rotates x-axis labels to avoid overlap
                title_standoff=20
            ),
            yaxis=dict(title="Sum of trips"),  # Y-axis title
            width=900,
            height=600
        )
    )

    # Display the bar chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Add in markdown comments
    st.markdown("""
    ### **Key Insights**
    - **Bike demand shifts seasonally**, impacting which stations receive the most trips.
    - **W 21 St & 6 Ave consistently ranks as the top station across all seasons**, with **West St & Chambers St** also maintaining high ridership.
    - **Winter:** Commuter-heavy stations like **1 Ave & E 68 St** see increased usage.
    - **Spring & Summer:** Tourist-friendly stations (**West St & Chambers St, Broadway & W 58 St**) experience a **surge in demand**.
    - **Fall:** Work commute patterns return, making **W 21 St & 6 Ave the leading station** again.
    
    ### **What This Means**
    - **Different seasons influence trip patterns**, requiring **seasonal bike redistribution**.
    - **Commuter vs. Tourist Impact:** Warm months see increased **tourist usage**, while **cold months favor work commuters**.
    
    ### **Next Step:**
    - Check out the **Conclusions and Recommendations** section to explore Citi Bike’s strategies for optimizing bike availability and station efficiency.
    """)

### Add the map ###

elif page == 'Interactive Map with Aggregated Bike Trips':

    # URL of the zipped HTML map stored in GitHub (update with your actual username/repo)
    html_zip_url = "https://github.com/jeff-frankenfeld/Citi_Bike_Dashboard/raw/main/05%20Sent%20to%20Client/Citi_Bike_Trips_Aggregated.zip"
    
    # Download the ZIP file from GitHub
    response = requests.get(html_zip_url)
    
    if response.status_code == 200:
        # Open the ZIP file
        with zipfile.ZipFile(BytesIO(response.content), 'r') as zip_ref:
            # Extract the HTML file inside the ZIP
            with zip_ref.open("Citi_Bike_Trips_Aggregated.html") as html_file:
                html_data = html_file.read().decode("utf-8")  # Read and decode the file content
    
        # Display the map in Streamlit
        st.subheader("🗺️ Aggregated Bike Trips in New York City")
        st.components.v1.html(html_data, height=1000)
    else:
        st.error("❌ Failed to load HTML map. Please check the GitHub link.")

    # Add in markdown comments
    st.markdown("""
    ### **Key Insights**
    - **Overlapping Stations Suggest Round Trips**
      - `W 21 St & 6 Ave` appears in both the **top start and end stations**, indicating **many riders return to the same location**.
      - This suggests that **casual riders often take round trips**, while **commuters utilize these loops for daily travel**.
    
    - **Central Park Dominance**
      - **4 of the top 5 routes are near Central Park**, confirming **Citi Bikes are heavily used for scenic rides and casual biking.**
    
    - **Roosevelt Island Usage**
      - **Roosevelt Island ranks as the third highest route**, showing **strong usage by both tourists and locals.**
    
    - **Top Commuter Corridors**
      - `W 21 St & 6 Ave → 9 Ave & W 22 St` is likely **a short work commute route in Chelsea.**
      - `1 Ave & E 62 St → 1 Ave & E 68 St` suggests **bike usage for last-mile connections between subway stations.**
    
    ### **What This Means**
    - **Round-trip rides are frequent in parks and Roosevelt Island.**
    - **Commuter-heavy routes exist in Chelsea and Midtown Manhattan.**
    
    ### **Next Step:**
    - Visit the **Conclusions and Recommendations** section to see Citi Bike’s strategies for optimizing bike availability and improving station infrastructure.
    """)

### Trips by Hour: Weekday vs Weekend page ##

elif page == "Trips by Hour: Weekday vs Weekend":
    st.header("Trip Frequency by Hour of Day (Weekday vs. Weekend)")

    # Cached function to preprocess data
    @st.cache_data
    def prepare_trip_data(df):
        # Check if 'started_at' exists
        if "started_at" not in df.columns:
            st.error("Column 'started_at' is missing from the dataset!")
            return pd.DataFrame()  # Return empty DataFrame to avoid errors

        # Ensure 'started_at' is in datetime format
        df["started_at"] = pd.to_datetime(df["started_at"], errors='coerce')

        # Drop rows where 'started_at' could not be converted
        df = df.dropna(subset=['started_at'])

        # Extract the hour
        df["hour"] = df["started_at"].dt.hour

        # Categorize into 'Weekday' or 'Weekend'
        df["day_type"] = df["started_at"].dt.day_name().map(
            lambda x: "Weekend" if x in ["Saturday", "Sunday"] else "Weekday"
        )

        # Aggregate trip counts
        df_subset = df.groupby(["hour", "day_type"]).size().reset_index(name="trip_count")

        return df_subset

    # Load preprocessed data
    df_subset = prepare_trip_data(df)

    # Stop execution if df_subset is empty
    if df_subset.empty:
        st.warning("No trip data available for this filter. Please adjust selections.")
        st.stop()

    # Split data into weekday and weekend for separate traces
    weekday_data = df_subset[df_subset["day_type"] == "Weekday"]
    weekend_data = df_subset[df_subset["day_type"] == "Weekend"]

    # Create a histogram using plotly.graph_objects (matching bar chart formatting)
    fig = go.Figure(
        data=[
            go.Bar(
                x=weekday_data["hour"],  # X-axis: Hours of the day
                y=weekday_data["trip_count"],  # Y-axis: Trip count
                name="Weekday Trips",  # Legend label
                marker={'color': 'blue'},  # Weekday color
            ),
            go.Bar(
                x=weekend_data["hour"],
                y=weekend_data["trip_count"],
                name="Weekend Trips",
                marker={'color': 'red'},  # Weekend color
            )
        ],
        layout=go.Layout(
            title="Trip Frequency by Hour of Day (Weekday vs. Weekend)",  # Chart title
            barmode="group",  # Group bars for comparison
            xaxis=dict(
                title="Hour of the Day",
                tickangle=-45,  # Rotate labels for readability
                dtick=1,  # Show every hour
                title_standoff=20
            ),
            yaxis=dict(title="Number of Trips"),  # Y-axis title
            width=900,
            height=600
        )
    )

    # Display the histogram in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Add in markdown comments
    st.markdown("""
    ### **Key Insights**
    
    - **Weekday Commuter Peaks**
      - **Two major spikes at 8 AM and 5-7 PM**, aligning with **work commute hours**.
      - Indicates **heavy use for first-mile/last-mile connections to transit hubs**.
    
    - **Steady Weekend Usage**
      - **Trips are more evenly distributed throughout the day**, peaking in the afternoon.
      - Suggests **recreational riders and tourists** use Citi Bikes for leisure activities.
    
    ### **What This Means**
    - **Weekday demand is driven by work commuters**, requiring **bike availability near business districts and transit hubs during peak hours**.
    - **Weekend demand is more recreational**, necessitating **higher availability at parks, greenways, and leisure destinations**.
    
    ### **Next Step:**
    - Visit the **Conclusions and Recommendations** section to see Citi Bike’s strategies for optimizing bike availability and meeting demand efficiently.
    """)

### Conclusions and Recommendations page ##

else:
    
    st.header("Conclusions and Recommendations")

    # URL of the outro image stored in GitHub (update with your actual username/repo)
    outro_image_url = "https://raw.githubusercontent.com/jeff-frankenfeld/Citi_Bike_Dashboard/main/05%20Sent%20to%20Client/Citi_Bikes_2.jpg"
    
    # Download the image from GitHub
    response = requests.get(outro_image_url)
    
    if response.status_code == 200:
        # Open the image
        outro_image = Image.open(BytesIO(response.content))
    
        # Display the image in Streamlit
        st.image(outro_image, use_column_width=True)
    else:
        st.error("❌ Failed to load outro image. Please check the GitHub link.")

    # Section Header: Key Takeaways
    st.subheader("Key Takeaways")

    st.markdown("""
    - **Seasonal Ridership Trends:** Demand **peaks in warm months** and declines in winter.
    - **High-Demand Stations:** `W 21 St & 6 Ave` is the most-used start station year-round.
    - **Recreational vs. Commuter Usage:** 
      - **Parks (Central Park, Roosevelt Island) see high leisure use.**
      - **Work commutes dominate Chelsea & Midtown routes.**
    - **Commuter Rush Hours:**  
      - **Weekday peaks at 8 AM & 5-7 PM (work commutes).**  
      - **Weekend ridership is steady, peaking in the afternoon.**
    """)

    # Divider for clarity
    st.markdown("---")

    # Section Header: Strategic Recommendations
    st.subheader("Strategic Recommendations")

    st.markdown("""
    **Optimize Seasonal Bike Deployment**  
    - Increase bike availability **near parks and tourist hotspots** from **spring to summer**.  
    - Prioritize commuter-heavy stations **in fall & winter** to match work patterns.  

    **Improve Bike Availability at High-Demand Locations**  
    - **Expand docking stations** near **Central Park & Roosevelt Island**.  
    - Ensure **full docks at transit hubs** during peak weekday hours.  

    **Enhance Real-Time Bike Management**  
    - Use **live data tracking** to predict demand and **prevent shortages**.  
    - Improve redistribution to **reduce station overcrowding**.  

    **Encourage Year-Round Ridership**  
    - **Offer seasonal discounts** for winter riders.  
    - Invest in **better bike infrastructure**, such as heated docking stations and helmet rentals.  
    """)