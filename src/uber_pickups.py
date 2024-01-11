import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC') # title

# Add url and column name
DATE_COLUMN = 'date/time' # column name
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz') # url

#
@st.cache_data # cache data
def load_data(nrows): # nrows: number of rows
    data = pd.read_csv(DATA_URL, nrows=nrows) # read data
    lowercase = lambda x: str(x).lower() # convert to lowercase
    data.rename(lowercase, axis='columns', inplace=True) # rename columns
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) # convert to datetime
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...') # text element
# Load 10,000 rows of data into the dataframe.
data = load_data(10000) # load data
# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache_data)") # text element

# Add checkbox for plot data on a table
if st.checkbox('Show raw data'): # add checkbox
    st.subheader('Raw data') # subheader
    st.write(data) # write data

# Plot data on a histogram
st.subheader('Number of pickups by hour') # subheader
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] # histogram
st.bar_chart(hist_values) # add bar chart

# Filter data by hour
# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17) # filter by hour slider
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter] # add filter data

# Plot the map
st.subheader('Map of all pickups at %s:00' % hour_to_filter) # subheader
st.map(filtered_data) # Plot data on a map