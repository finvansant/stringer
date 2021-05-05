import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

def page_clusters():

    st.text('page_clusters')

    DATA_URL = ('data/cluster_tweets.csv')

    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        data['created_on']= pd.to_datetime(data['created_on'])
        data['clusters'] += 1
        return data


    # Create a text element and let the reader know the data is loading.
    data_load_state = st.text('Loading data...')

    # Load 10,000 rows of data into the dataframe.
    data = load_data(1000)

    # Notify the reader that the data was successfully loaded.
    data_load_state.text("Done! (using st.cache)")


    # Load clusters CSV
    df_clusters = pd.read_csv('data/cluster_keywords.csv', index_col=0)

    st.subheader('Explore Clusters')
    st.write("")
    st.write("Top keywords for each cluster:")
    st.write(df_clusters)
    st.write("")
    st.write("")
    st.write("Summary statistics for each cluster:")

    # Show statistics about the different clusters (total audience, total number of posts)

    dfsumfollowers = data[["clusters", "user_follower_count"]]
    dfsumfollowers = dfsumfollowers.groupby(["clusters"], as_index = False).sum()
    dfsumfollowers = dfsumfollowers.rename(columns={"user_follower_count":"total_followers"})

    dfcountposts = data[["clusters", "user_follower_count"]]
    dfcountposts = dfcountposts.groupby(["clusters"], as_index = False).count()
    dfcountposts = dfcountposts.rename(columns={"user_follower_count":"total_number_of_posts"})

    dfsummary = pd.merge(dfsumfollowers, dfcountposts, on="clusters")
    dfsummary['average_audience'] = round((dfsummary['total_followers'] / dfsummary['total_number_of_posts']))
    dfsummary = dfsummary.rename(columns={"clusters":"Cluster", "total_followers":"Total Followers", "total_number_of_posts":"Total Posts", "average_audience":"Average Audience"})

    st.write(dfsummary)

    st.write("")
    st.write("")

    st.write('Cluster map visualization:')
    st.image('./images/cluster_map_visualization.png')

    st.subheader('Explore Tweets')

    # User selection of cluster
    cluster_choice = st.selectbox(
    'Which cluster would you like to explore further?',
    df_clusters.columns)

    st.write('You selected:', cluster_choice)

    # Reorganize tweet data
    data2 = data[["clusters", "tweet_text", "user", "user_follower_count", "hashtags"]]
    data2 = data2.rename(columns={"clusters":"Cluster", "tweet_text":"Tweet Text", "user":"User", "user_follower_count":"Followers", "hashtags":"Hashtags"})

    # Filter based on cluster choice input
    st.write(data2[data2["Cluster"] == int(cluster_choice[-1])])


    # Create a time series of tweets

    # ----------------------

    # Load timeseries data
    df_time = pd.read_csv('data/time_series.csv')

    from datetime import date
    from datetime import datetime
    time_cluster = df_time[df_time['cluster'] == int(cluster_choice[-1])-1][['Date','Velocity']]

    min_time = datetime.strptime(min(time_cluster['Date']), '%Y-%m-%d')
    max_time = datetime.strptime(max(time_cluster['Date']), '%Y-%m-%d')

    timerange = st.slider("Select Time Range:",min_value=min_time, max_value=max_time,value=(min_time, max_time),format="YY-MM-DD")

    c = alt.Chart(time_cluster[(time_cluster['Date']>=timerange[0].strftime('%Y-%m-%d')) & (time_cluster['Date']<=timerange[1].strftime('%Y-%m-%d'))])\
    .mark_area(color='lightblue',point=True).encode(x='Date',y='Velocity')
    st.altair_chart(c,use_container_width=True)

    # ----------------------

    # Show full dataframe on user request
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    # Spacing
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    return
