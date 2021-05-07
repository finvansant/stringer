import streamlit as st

from page_introduction import page_introduction
from page_clusters import page_clusters
from page_velocity import page_velocity
from page_team import page_team
from page_novelty import page_novelty
from datetime import date

# Sidebar
st.sidebar.image('./images/cornell_tech_logo.png')

st.sidebar.title("Navigation")

sidebar_pages = {
    "Introduction": page_introduction,
    "Novelty": page_novelty,
    "Relevant Topics": page_clusters,
    "Velocity": page_velocity,
    "Team": page_team
}

page = st.sidebar.radio("Select:", tuple(sidebar_pages.keys()))

sidebar_pages[page]()
