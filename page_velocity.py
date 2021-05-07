import streamlit as st
import pandas as pd
import altair as alt

def page_velocity():

    st.text('page_velocity')

    st.subheader('Explore Velocity')
    st.write("")
    st.write("To understand how a topic is developing over time, you can explore the changes between clusters on a week-by-week basis. The first table simply shows a comparison of the different keywords in each cluster of each week.")
    st.write("")

    # State changes of clusters
    st.write("Top keywords for each cluster:")
    df_clustersEvolution = pd.read_csv('data/velocity_page/clustersEvolution.csv', index_col=0)
    st.write(df_clustersEvolution)
    st.write("")
    st.write("By comparing the number of posts within each cluster, you can see if a topic is getting more or less popular compared to the previous week. Similarly looking at the change in number of users within the cluster also gives a sense for the size of the group talking about a particular topic.")
    st.write("")
    st.write("")

    # Percentage change within evolved clusters
    st.write("Percentage change within evolved clusters:")
    st.write("")
    df_percentageChange = pd.read_csv('data/velocity_page/evolvedClustersPercentChange.csv', index_col=0)
    st.write(df_percentageChange)

    st.write("")
    st.write("Of course, some clusters are completely new. This table shows these clusters, with the same summary statistics as you can see on the original 'cluster' page")
    st.write("")

    # Statistics regarding new clusters
    st.write("Statistics regarding new clusters:")
    st.write("")
    df_newClusterStats = pd.read_csv('data/velocity_page/newClustersStats.csv', index_col=0)
    st.write(df_newClusterStats)
    
    st.write("")
    st.write("")
    st.write("")
    expander = st.beta_expander("How are clusters connected to each other?")
    expander.markdown("As the clustering algorithm starts from scratch each time, clusters are not consistent from each analysis of the topic. Instead, we calculate the overlapping keywords between different clusters. If 50 percent of the keywords are the same, the cluster continues.")



    return
