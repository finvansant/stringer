import streamlit as st
import pandas as pd
import altair as alt

def page_velocity():

    st.text('page_velocity')

    df_velocity = pd.read_csv('data/velocity_page/clustersEvolution.csv', index_col=0)

    st.subheader('Work in Progress!')



    return
