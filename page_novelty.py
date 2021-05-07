import streamlit as st
import pandas as pd

def page_novelty():

    st.subheader('Explore Novelty')
    st.write("")
    st.write("")
    st.write("To introduce novelty and ensure customer-provided search terms do not narrow the scope of results, we compute the Jaccard coefficient between each customer input term and existing terms in our database. We then expand the search query to include related terms that have a Jaccard coefficient greater than 0.005 with any of the customer-provided terms.")
    st.image('images/search_term.png')
    st.write("")

    st.text('Jaccard analysis for overall search terms:')

    df_jaccard_hashtags = pd.read_csv('data/novelty_page/jaccard_hashtags.csv', index_col=0)

    st.write(df_jaccard_hashtags)
    st.write("")
    st.write("It's worth looking at this initial pass for novelty, as the Jaccard analysis can sometimes produce pairs of words that are unexpected. These unusual pairs can be a good sign that a topic is of interest.")
    st.write("")

    return
