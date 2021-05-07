import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

def page_velocity():

    st.subheader('Explore Velocity')
    st.write("")
    st.write("To understand how a topic is developing over time, you can explore the changes between clusters on a week-by-week basis. The first table simply shows the clusters that failed to evolve week to week and were instead depreciated.")
    st.write("")

    # State changes of clusters
    st.write("Depreciated clusters:")
    df_depreciatedClusters = pd.read_csv('data/velocity_page/clustersEvolution.csv', index_col=0)
    st.dataframe(df_depreciatedClusters)

    # Percentage change within evolved clusters
    st.write("Evolved clusters:")
    df_evolvedClusters = pd.read_csv('data/velocity_page/evolvedClustersPercentChange.csv', index_col=0)
    st.write(df_evolvedClusters)

    st.write("")
    st.write("Of course, some clusters are completely new. This table shows these clusters, with the same summary statistics as you can see on the original 'cluster' page")
    st.write("")

    # Statistics regarding new clusters
    st.write("New clusters:")
    df_newClusters = pd.read_csv('data/velocity_page/newClustersStats.csv', index_col=0)
    st.write(df_newClusters)

    st.write("")
    st.write("")
    st.write("")
    expander = st.beta_expander("How are clusters connected to each other?")
    expander.markdown("As the clustering algorithm starts from scratch each time, clusters are not consistent from each analysis of the topic. Instead, we calculate the overlapping keywords between different clusters. If 50 percent of the keywords are the same, the cluster continues.")

    data = df_evolvedClusters


    return
