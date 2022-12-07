import streamlit as st
import pandas as pd
import datetime as dt
import last_run as lr
import timedelta as td
import plotly.express as px
from milestone_tab import milestone
from overview_tab import overview
from team_graph_tab import team_graph


st.set_page_config(
    page_title= 'DADS Fitness Challenge', 
    layout="wide", 
    page_icon= ':sports_medal:'
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
    st.write('')
    strava_widget = "<h3><iframe allowtransparency frameborder='0' height='300' scrolling='yes' src='https://www.strava.com/clubs/995662/latest-rides/84e66ad0283c10bf7ace6e5b31be4058becca9c3?show_rides=false' width='285'></iframe></h3>"
    st.markdown(strava_widget, unsafe_allow_html=True)


tab1, tab2, tab3, tab4 = st.tabs(['Team Standings','Activities Overview', 'Milestones Achievement', 'General Information'])

with tab1:  
    team_graph()
    
with tab2:
    overview()
    
   
with tab3:
    milestone()
    
with tab4:
    st.subheader('Links')
    url='https://www.strava.com/clubs/DCFC'
    st.write("[Strava Club](%s)" % url)
    
    
    st.subheader('Downloads')

    with open("data/rulebook.pdf", "rb") as pdf_file:
        pdf = pdf_file.read()
        
    st.download_button(label="Download Rulebook",
                       data=pdf,
                       file_name="Rulebook.pdf",
                       mime='application/octet-stream')
        
    with open("data/Fitness Challenge.pdf", "rb") as pdf_file:
        pdf = pdf_file.read()

    st.download_button(label="Download Points Calculation Overview",
                       data=pdf,
                       file_name="Fitness Challenge.pdf",
                       mime='application/octet-stream')
    
    st.subheader('Contacts')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('***If you have any questions contact:***')
        st.write('Subramita Dash - subramita_dash@dell.com')
        st.write('Madhav Parashar - madhav_parashar@dell.com')
        st.write('Sanjay Kumar - sanjay_kumar29@dell.com')
        st.write('Ivana Kovacova - ivana.kovacova@dell.com')
    with col2:
        st.markdown('***For issues with the app:***')
        st.write('Ivana Kovacova - ivana.kovacova@dell.com')
       

col1, col2, col3 = st.columns(3)


last_run = lr.get_last_run_time_stamp()
now = dt.datetime.utcnow()
dif = (now - last_run)
dif_time = td.format_timedelta(dif)

with col3:
    st.header('')
    st.write(f'Last data update: {dif_time} ago')

