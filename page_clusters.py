import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
from datetime import date
from datetime import datetime

def page_clusters():

    # st.text('page_clusters')

    DATA_URL = ('data/clusters_page/cluster_tweets.csv')

    @st.cache
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        data['created_on']= pd.to_datetime(data['created_on'])
        data['clusters'] += 1
        return data


    # Create a text element and let the reader know the data is loading.
    # data_load_state = st.text('Loading data...')

    # Load 10,000 rows of data into the dataframe.
    data = load_data(5000)
    # Notify the reader that the data was successfully loaded.
    # data_load_state.text("Done! (using st.cache)")

    #d = st.sidebar.date_input("Date",date(2021, 4, 29))

    # Load clusters CSV
    df_clusters = pd.read_csv('data/clusters_page/cluster_keywords.csv', index_col=0)
    df_clusters.columns=["Cluster "+str(i) for i in range(1, df_clusters.shape[1] + 1)]

    st.subheader('Explore Relevant Topics Through Clusters')
    st.write("")
    st.write("The table below shows the keywords that best describe each cluster so are a good way to understand the overall topic, and compare the different types of commentary on social media.")
    st.write("")
    st.write("Top keywords for each cluster on April 29th 2021:")
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
    dfsummary = dfsummary.rename(columns={"clusters":"Cluster", "total_number_of_posts":"Total Posts", "total_followers":"Total Followers", "average_audience":"Average Audience"})

    dfsummary = dfsummary[['Cluster', 'Total Posts', 'Total Followers', 'Average Audience']]
    dfsummary['Cluster'].replace({1:'Cluster 1',2:'Cluster 2',3:'Cluster 3',4:'Cluster 4',5:'Cluster 5',6:'Cluster 6',7:'Cluster 7'},inplace=True)
    dfsummary.set_index('Cluster', inplace=True)
    st.write(dfsummary)

    st.write("")
    st.write("")

    st.write('Cluster map visualization:')

    cluster_3d = data[['pc1','pc2','pc3','label','tweet_text','retweet_count']]
    cluster_3d.sort_values(by=['label'],inplace=True)
    cluster_3d['tweet_text'] = cluster_3d['tweet_text'].str.wrap(30).apply(lambda x: x.replace('\n', '<br>'))
    cluster_3d['label'] = cluster_3d['label'] .astype(object)


    fig = px.scatter_3d(
        cluster_3d, x='pc1', y='pc2', z='pc3', color=cluster_3d['label'],
        hover_data = {'label':True, 'tweet_text':True,'pc1':False, 'pc2':False, 'pc3':False,'retweet_count':True},
        template = 'plotly_white'
    )
    cluster_3d['retweet_count'] = cluster_3d['retweet_count'] + 1
    fig.update_traces(marker=dict(size=cluster_3d['retweet_count'],sizemode='area',sizeref=8))
    fig.update_traces(hoverlabel_font_size=12)
    fig.update_layout(width=250,
        scene=dict(
        xaxis=dict(showticklabels=False,visible=False),
        yaxis=dict(showticklabels=False,visible=False),
        zaxis=dict(showticklabels=False,visible=False),)
    )

    st.plotly_chart(fig, use_container_width=True,height=250)
    st.write("")


    st.subheader('Dive Deeper Into One Cluster')
    st.write("")
    st.write("Go deeper into the cluster by looking at individual tweets, and see how the clusters grew over time using the timeseries chart.")
    st.write("")

    # User selection of cluster
    cluster_choice = st.selectbox(
    'Which cluster would you like to explore further?',
    df_clusters.columns)

    st.write('You selected:', cluster_choice)

    # Reorganize tweet data
    data2 = data[["clusters", "tweet_text", "user", "user_follower_count",'retweet_count', "created_on","hashtags"]]
    data2['created_on'] = data2['created_on'].astype(str).str[:10]
    data2 = data2.rename(columns={"clusters":"Cluster", "tweet_text":"Tweet Text", "user":"User", "user_follower_count":"Followers", "hashtags":"Hashtags","retweet_count":"Retweet Counts"})

    st.write("")
    st.write("Full tweets within this cluster:")

    # Filter based on cluster choice input
    st.write(data2[data2["Cluster"] == int(cluster_choice[-1])].drop(['Cluster'],axis=1))
    st.write("")
    st.write("")

    col1, col2 = st.beta_columns(2)
    cluster_followers = data2[data2["Cluster"] == int(cluster_choice[-1])].drop_duplicates(subset='User')
    fig = px.scatter(cluster_followers, x='Cluster',y='Followers',size='Followers',hover_data=['User'],template = 'plotly_white')
    fig.update_traces(marker_color='orange',marker=dict(sizemode='area',sizeref=5000))
    fig.update_xaxes(visible=False, showticklabels=False,range=[int(cluster_choice[-1])-1,int(cluster_choice[-1])+1])
    col1.plotly_chart(fig, use_container_width=True)


    cluster_retweets = data2[data2["Cluster"] == int(cluster_choice[-1])]
    cluster_retweets['Tweet Text'] = cluster_retweets['Tweet Text'].str.wrap(20).apply(lambda x: x.replace('\n', '<br>'))
    fig = px.scatter(cluster_retweets, x='Cluster',y='Retweet Counts',size='Retweet Counts',hover_data=['Tweet Text'],template = 'plotly_white')
    fig.update_traces(marker_color='orange',marker=dict(sizemode='area',sizeref=50))
    fig.update_xaxes(visible=False, showticklabels=False,range=[int(cluster_choice[-1])-1,int(cluster_choice[-1])+1])
    fig.update_traces(hoverlabel_font_size=10)
    col2.plotly_chart(fig, use_container_width=True)

    st.write("")
    st.write("")
    st.write("Number of tweets over time:")
    st.write("")
    # Create a time series of tweets

    # ----------------------

    # Load timeseries data
    df_time = pd.read_csv('data/clusters_page/time_series.csv')


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
    #FAQ
    st.subheader("FAQ")
    expander = st.beta_expander("What is the source for this data?")
    expander.markdown("Data is acquired using the Twitter Search API")
    expander = st.beta_expander("What do the different columns mean?")
    expander.write("For detailed explanations check out the Twitter Search API documentation.")
    expander = st.beta_expander("Who do I contact for help with this information?")
    expander.write("Feel free to reach out to the Stringer Team!")

    st.write("")
    st.write("")
    st.write("")

    return
