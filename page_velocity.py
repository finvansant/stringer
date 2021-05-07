import streamlit as st
import pandas as pd
import altair as alt

def page_velocity():

    st.subheader('Explore Velocity Through Cluster Comparison')
    st.write("")
    st.write("To understand how a topic is developing over time, you can explore the changes between clusters on a week-by-week basis. The first table simply shows the clusters that failed to evolve week to week and were instead depreciated.")
    st.write("")

    # Depreciated Clusters
    st.write("Depreciated clusters:")
    df_depreciatedClusters = pd.read_csv('data/velocity_page/depreciatedClusters.csv', index_col=0)
    st.dataframe(df_depreciatedClusters)

    # Evolved Clusters
    st.write("")
    st.write("Evolved clusters:")
    df_evolvedClustersGraph = pd.read_csv('data/velocity_page/evolvedClustersGraph.csv', index_col=0)
    st.write("")
    st.write("The second table consists of clusters that have evolved from one week to the next (April 22nd 2021 to April 29nd 2021), these clusters have evolved across both metrics and within the keywords themselves.")
    st.write("")
    st.write(df_evolvedClustersGraph)

    # Drop keywords from Chart
    to_drop = ['Keyword 1','Keyword 1', 'Keyword 2', 'Keyword 3', 'Keyword 4', 'Keyword 5', 'Keyword 6', 'Keyword 7', 'Keyword 8', 'Keyword 9', 'Keyword 10']
    df_evolvedClustersGraph.drop(to_drop, inplace=True, axis=1)

    # Dropdown Filter
    views = ['number of tweets', 'number of users', 'favorite count', 'number of followers', 'number of verified followers', 'average number of tweets']
    views_dropdown = alt.binding_select(options=views, name='view')
    views_select = alt.selection_single(fields=['views'], bind=views_dropdown, init={'views': 'number of tweets'})

    # Evolved Clusters Chart
    alt_velocity_chart = alt.Chart(df_evolvedClustersGraph).mark_line().encode(
        x='date:Q',
        y='instance:Q',
        strokeDash='Clusters',
    ).add_selection(
        views_select
    ).transform_filter(
        views_select
    )

    st.write("")
    st.write("")
    st.altair_chart(alt_velocity_chart, use_container_width=True)
    st.write("")
    st.write('To further explore the cluster evolution, look at the metrics changes through the filtered views dropdown.')

    st.write("")
    st.write("Of course, some clusters are completely new. This table shows these clusters, with the same summary statistics as you can see on the original 'cluster' page")
    st.write("")

    # New Clusters
    st.write("New clusters:")
    df_newClusters = pd.read_csv('data/velocity_page/newClusters.csv', index_col=0)
    st.write(df_newClusters)

    st.write("")
    st.write("")
    st.write("")
    expander = st.beta_expander("How are clusters connected to each other?")
    expander.markdown("As the clustering algorithm starts from scratch each time, clusters are not consistent from each analysis of the topic. Instead, we calculate the overlapping keywords between different clusters. If 50 percent of the keywords are the same, the cluster continues.")

    return
