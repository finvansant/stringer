import streamlit as st
import pandas as pd
import numpy as np

from page_introduction import page_introduction
from page_clusters import page_clusters
from page_velocity import page_velocity
from page_team import page_team

# Sidebar
st.sidebar.image('./images/cornell_tech_logo.png')

sidebar_pages = {
    "Introduction": page_introduction,
    "Explore Clusters": page_clusters,
    "Velocity": page_velocity,
    "Team": page_team
}

st.sidebar.title("Navigation")

page = st.sidebar.radio("Select:", tuple(sidebar_pages.keys()))

sidebar_pages[page]()

st.image('./images/stringer_logo.png')
st.title('Surfacing Viral Misinformation')



# Spacing
st.write("")
st.write("")
st.write("")

DATA_URL = ('data/2021-04-28-19-34-42-FP_500_streamlistener.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data['created_on']= pd.to_datetime(data['created_on'])
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')

# Load 10,000 rows of data into the dataframe.
data = load_data(500)

# Notify the reader that the data was successfully loaded.
data_load_state.text("Done! (using st.cache)")

data.dtypes


# Load clusters CSV
df_clusters = pd.read_csv('data/2021-04-28-19-34-42-FP_500search.csv', index_col=0)

st.subheader('Explore clusters')
df_clusters

# User selection of cluster
cluster_choice = st.selectbox(
    'Which cluster would you like to explore further?',
    df_clusters.columns)

st.write('You selected:', cluster_choice)

st.subheader('Explore tweets')

# Reorganize tweet data
data2 = data[["clusters", "tweet_text", "user", "user_follower_count", "hashtags"]]

# Filter based on cluster choice input
st.write(data2[data2["clusters"] == int(cluster_choice[-1])])


# Create a time series of tweets

"""data_timeindex = data.set_index('created_on')
data_timeindex = data_timeindex[["tweet_text", "clusters"]]
data_timeindex
st.line_chart(data_timeindex)"""

# Show full dataframe on user request
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)
