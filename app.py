import folium 
import seaborn as sns 
import matplotlib.pyplot as plt 
import pandas as pd
import streamlit as st
import numpy as np 
import mysql.connector
from sshtunnel import SSHTunnelForwarder
import datetime
import plotly.express as px
from datetime import date, timedelta, datetime
import plotly.graph_objs as go
from streamlit_folium import folium_static
from PIL import Image
import time
from getdata import temperature
import random

st.set_page_config(layout="wide",
                   initial_sidebar_state="expanded")

temp, weather = temperature()
welcome = ['Good Morning', 'Hi', 'Hello','Good Afternoon']



image = Image.open('logo-lg (1).png')

st.image(image)

def get_time_of_day(time):
    if time < 12:
        st.write('Good Morning, How are you today? :smile:')
    elif time > 12 & time < 17:
        st.write('Good Afternoon, How are you today? :smile:')
    else:
        st.write(f'{random.choice(welcome[1:3])} Eric, How are you today? :smile:')
current_hour = datetime.now().hour
get_time_of_day(current_hour)

weather_emojis = {
    "Clear": "\u2600",
    "Clouds": "\u2601",
    "Rain": "\U0001F327",
    "Snow": "\u2744",
    "Thunderstorm": "\u26C8",
    "Drizzle": "\U0001F326",
    "Fog": "\U0001F32B",
    "Haze": "\u2591",
    "Smoke": "\U0001F32B",
    "Tornado": "\U0001F32A",
}

# Get the emoji for the current weather
current_emoji = weather_emojis.get(weather, '')

st.write(f'Greater Sudbury, {temp}℃ {weather} {current_emoji}')

df = pd.read_csv('filtered_data.csv')

st.header("Welcome to Demo Call Detail Record")

df['StartTime'] = pd.to_datetime(df['StartTime'])
df['EndTime'] = pd.to_datetime(df['EndTime'])

df['date'] = df['StartTime'].dt.date
min_date = df['date'].min()
max_date = df['date'].max()
default_end_date = min_date + timedelta(days=30)  # Default end date 30 days after the min_date


toll_processed = df['TollProcessed'].unique().tolist()



selected_dates = st.sidebar.date_input(
    "Select a date range:",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)


#Calculate number of call per hour.
min_date_time = df['StartTime'].min()
selected_date = st.sidebar.date_input("Select a date:", min_date_time.date())
selected_time = st.sidebar.time_input("Select a time:", min_date_time.time())



selected_date_time = datetime.combine(selected_date, selected_time)
# Filter the dataset to include only calls that started on the selected date and hour
filtered_df = df[(df['StartTime'].dt.date == selected_date_time.date()) &
                 (df['StartTime'].dt.hour == selected_date_time.hour)]


disposition = df['Disposition'].unique().tolist()
options = st.sidebar.multiselect(
    "Disposition",
    disposition
)

options_2 = st.sidebar.radio(
    "Toll Processed",
     toll_processed
)


number_of_calls = len(filtered_df)

previous_hour_date_time = selected_date_time - timedelta(hours=1)
previous_hour_filtered_df = df[(df['StartTime'].dt.date == previous_hour_date_time.date()) &
                               (df['StartTime'].dt.hour == previous_hour_date_time.hour)]
number_of_calls_previous_hour = len(previous_hour_filtered_df)
call_difference = number_of_calls - number_of_calls_previous_hour




if len(selected_dates) != 2:
    st.error("Please select a valid date range!")
else:
    start_date, end_date = selected_dates

    

    # Filter the dataset based on the selected date range
    start_date, end_date = selected_dates
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
     # Filter the DataFrame based on the selected dispositions
    if options:
        filtered_df = filtered_df[filtered_df['Disposition'].isin(options)]
    total_call = len(filtered_df)
    call_different = len(filtered_df) - len(df[(df['date'] == start_date)])

    if options_2:
        filtered_df = filtered_df[filtered_df['TollProcessed'].isin(options)]
    total_call = len(filtered_df)
    call_different = len(filtered_df) - len(df[(df['date'] == start_date)])


    col1,col2,col3,coln,colm = st.columns(5)
    with st.container():
        try:
            if start_date < df['date'].min():
                st.write(f"Your First Calls Start From {df['date'].min()}")
            else:
                col1.metric("Total Number of Calls", f"{total_call}", call_different)
        except ValueError:
            st.error("Please select a valid date range!")
    col2.metric('Number of user', 100000, 80000)
    col3.metric('Percenatege of Customer Churn', 1000, -999)
    coln.metric("Number of call per hours", f"{number_of_calls}", call_difference)
    colm.metric("Avg Handle Time Per Call", 30, 35)

# col3,col4 = st.columns(2)
# Group the filtered data by date and count the number of calls per date
calls_by_date = filtered_df.groupby('date')['CallID'].count().reset_index()
st.divider()
# Create columns with custom widths
col3, col4,col9 = st.columns([3, 3,3])

if options:
    filtered_df = filtered_df[filtered_df['Disposition'].isin(options)]
with col3:
    st.write("<h5 style='text-align: center;'>Total Calls Over Time</h2>",unsafe_allow_html=True)
    calls_by_date = filtered_df.groupby(filtered_df['StartTime'].dt.date)['CallID'].count().reset_index(name='CallID')
    fig = go.Figure(go.Scatter(x=calls_by_date['StartTime'], y=calls_by_date['CallID'], mode='lines'))
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)
    st.plotly_chart(fig)
    
with col4:
    disposition_counts = filtered_df['Disposition'].value_counts().reset_index()


    # Rename the columns for better readability
    disposition_counts.columns = ['Disposition', 'Count']
    st.write("<h5 style='text-align: center;'>Distribution of Disposition</h2>",unsafe_allow_html=True)
    fig2 = go.Figure(go.Bar(x=disposition_counts['Disposition'], y=disposition_counts['Count']))
    fig2.update_xaxes(showgrid=False)
    fig2.update_yaxes(showgrid=False)
    st.plotly_chart(fig2)
with col9:
    toll_summary = df.groupby('TollProcessed')['CallID'].count().reset_index(name='Count')

    # Create a donut chart using Plotly
    fig = go.Figure(go.Pie(labels=toll_summary['TollProcessed'],
                        values=toll_summary['Count'],
                        hole=.3))

    # Customize the chart
    fig.update_traces(textinfo='percent', marker=dict(line=dict(color='#000000', width=2)))

    st.write("<h5 style='text-align: center;'>Toll Processed</h2>",unsafe_allow_html=True)

    # Display the donut chart in Streamlit
    st.plotly_chart(fig)



st.divider()

col5, col6 = st.columns([3, 2])
# Coordinates for Sudbury, Ontario, Canada
with col5:
    latitude = 46.4917
    longitude = -80.9930

    num_points = 1000
    latitudes = np.random.uniform(latitude - 0.05, latitude + 0.05, num_points)
    longitudes = np.random.uniform(longitude - 0.05, longitude + 0.05, num_points)
    random_points = pd.DataFrame({'lat': latitudes, 'lon': longitudes})
    number_of_points_to_show = st.sidebar.slider("The Location of Last 1000 Calls", min_value=1, max_value=len(random_points), value=10)
    sudbury_map = folium.Map(location=[latitude, longitude], zoom_start=12)

    for layer in ['OpenStreetMap', 'Stamen Terrain', 'Stamen Toner', 'Stamen Watercolor', 'CartoDB positron', 'CartoDB dark_matter']:
        folium.TileLayer(layer).add_to(sudbury_map)

    filtered_random_points = random_points.sample(number_of_points_to_show)
    for index, row in filtered_random_points.iterrows():
        folium.CircleMarker(
            [row['lat'], row['lon']],
            radius=1,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.7
        ).add_to(sudbury_map)


    folium.LayerControl().add_to(sudbury_map)
    st.write("<h5 style='text-align: center;'>Map of Sudbury with Random Points</h2>",unsafe_allow_html=True)
    folium_static(sudbury_map)

df['day_of_week'] = df['StartTime'].dt.day_name()
filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
with col6:
    day_order_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    calls_by_day_hour = filtered_df.groupby([filtered_df['day_of_week'], filtered_df['StartTime'].dt.hour])['CallID'].count().reset_index(name='CallCount')

    # Pivot the DataFrame
    calls_by_day_hour = calls_by_day_hour.pivot(index='day_of_week', columns='StartTime', values='CallCount').fillna(0)

    # Reindex the DataFrame based on the day_order_list
    calls_by_day_hour = calls_by_day_hour.reindex(day_order_list)
    plt.figure(figsize=(10, 5))
    sns.heatmap(calls_by_day_hour, annot=False, fmt='d', linewidths=.5)
    plt.title('Number of Calls by Day of the Week and Hour of the Day')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Day of the Week')
    st.pyplot(plt)



