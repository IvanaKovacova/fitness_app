import streamlit as st
import pandas as pd
import datetime as dt
import last_run as lr
import timedelta as td
from milestone_tab import milestone
from overview_tab import overview
from team_graph_tab import team_graph


st.set_page_config(
    page_title= 'DADS 100 days fitness challenge', 
    page_icon = '🏃',
    layout="wide"
    )

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage] {
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
    )

with st.sidebar:
    st.image("img/logo.png", width=150)
    st.header('')     

tab1, tab2, tab3 = st.tabs(['Overview', 'Graphs & Comparison', 'Milestones Achievement'])

with tab1:  
    overview()
    
with tab2:
    team_graph()
    
   
with tab3:
    milestone()
        

last_run = lr.get_last_run_time_stamp()
now = dt.datetime.utcnow()
dif = (now - last_run)
dif_time = td.format_timedelta(dif)
st.header('')
st.write(f'Last data update: {dif_time} ago')