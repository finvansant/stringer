import streamlit as st
import pandas as pd

def page_novelty():

    st.text('page_novelty')

    st.text('Jaccard analysis for overall search terms:')

    df_jaccard_hashtags = pd.read_csv('data/novelty_page/jaccard_hashtags.csv', index_col=0)

    st.write(df_jaccard_hashtags)


    return
