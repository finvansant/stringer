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
    df_clusters.columns=["Cluster "+str(i) for i in range(1, df_clusters.shape[1] + 1)]

    st.subheader('Explore Clusters')
    st.write("")
    st.write("The table below shows the keywords that best describe each cluster so are a good way to understand the overall topic, and compare the different types of commentary on social media.")
    st.write("")
    st.write("Top keywords for each cluster:")
    st.write(df_clusters)
    st.write("")
    st.write("To explore further, the table below shows information about the audience that was reached by tweets in each cluster. Click on a column name to sort by that column.")
    st.write("")
    st.write("Summary statistics for each cluster:")
    st.write("")


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
    st.write("")
    st.image('./images/cluster_map_visualization.png')

    st.subheader('Explore Tweets')

    st.write("")
    st.write("Go deeper into the cluster by looking at individual tweets, and see how the clusters grew over time using the timeseries chart.")
    st.write("")

    # User selection of cluster
    cluster_choice = st.selectbox(
    'Which cluster would you like to explore further?',
    df_clusters.columns)

    st.write('You selected:', cluster_choice)

    # Reorganize tweet data
    data2 = data[["clusters", "tweet_text", "user", "user_follower_count", "hashtags"]]
    data2 = data2.rename(columns={"clusters":"Cluster", "tweet_text":"Tweet Text", "user":"User", "user_follower_count":"Followers", "hashtags":"Hashtags"})

    st.write("")
    st.write("Full tweets within this cluster:")

    # Filter based on cluster choice input
    st.write(data2[data2["Cluster"] == int(cluster_choice[-1])])

    st.write("")
    st.write("")
    st.write("Number of tweets over time:")
    st.write("")
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
    st.write("")
    c = alt.Chart(time_cluster[(time_cluster['Date']>=timerange[0].strftime('%Y-%m-%d')) & (time_cluster['Date']<=timerange[1].strftime('%Y-%m-%d'))])\
    .mark_area(color='lightblue',point=True).encode(x='Date',y='Velocity')
    st.altair_chart(c,use_container_width=True)
    st.write("")
    st.write("")
    # ----------------------
    st.write("")
    st.write("Finally, if you'd want to dig deeper into the data, you can see all of the information about a tweet, and the user who posted it, here:")
    st.write("")
    # Show full dataframe on user request
    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(data)

    # Spacing
    st.write("")
    st.write("")
    st.write("")
    st.write("")

    # FAQ
    st.subheader("FAQ")
    expander = st.beta_expander("What is the source for this data?")
    expander.write("Answer1")
    expander = st.beta_expander("What do the different columns mean?")
    expander.write("Answer1")    
    expander = st.beta_expander("Who do I contact for help with this information?")
    expander.write("Answer1")


    st.write("")
    st.write("")

    return
