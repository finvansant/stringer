import streamlit as st
import pandas as pd
import altair as alt

def page_velocity():

    st.text('page_velocity')

    st.subheader('Explore Velocity')
    st.write("")


    # State changes of clusters
    st.write("Top keywords for each cluster:")
    df_clustersEvolution = pd.read_csv('data/velocity_page/clustersEvolution.csv', index_col=0)
    st.write(df_clustersEvolution)



    # Percentage change within evolved clusters
    st.write("Percentage change within evolved clusters:")
    df_percentageChange = pd.read_csv('data/velocity_page/evolvedClustersPercentChange.csv', index_col=0)
    st.write(df_percentageChange)

    # Statistics regarding new clusters
    st.write("Statistics regarding new clusters")
    df_newClusterStats = pd.read_csv('data/velocity_page/newClustersStats.csv', index_col=0)
    st.write(df_newClusterStats)





    return
