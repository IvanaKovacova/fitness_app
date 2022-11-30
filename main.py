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
    page_title= 'DADS 100 days fitness challenge', 
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
    
    strava_widget = "<h3><iframe allowtransparency frameborder='0' height='300' scrolling='no' src='https://www.strava.com/clubs/995662/latest-rides/84e66ad0283c10bf7ace6e5b31be4058becca9c3?show_rides=false' width='300'></iframe></h3>"
    st.markdown(strava_widget, unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(['Overview', 'Graphs & Comparison', 'Milestones Achievement', 'General Information'])

with tab1:  
    overview()
    
with tab2:
    team_graph()
    
   
with tab3:
    milestone()
    
with tab4:
    st.subheader('Information')
    st.write('PDF with point calculation overview:')
    with open("data/Fitness Challenge.pdf", "rb") as pdf_file:
        pdf = pdf_file.read()

    st.download_button(label="Download PDF",
                       data=pdf,
                       file_name="Fitness Challenge.pdf",
                       mime='application/octet-stream')
    
    st.subheader('Contacts')
    st.markdown('***Issues with the app:***')
    st.write('>Ivana Kovacova - ivana.kovacova@dell.com')
    st.markdown('***Other issues:***')
    st.write('>Subramita Dash - subramita_dash@dell.com')
    st.write('>Madhav Parashar - madhav_parashar@dell.com')
    st.write('>Sanjay Kumar - sanjay_kumar29@dell.com')
    st.write('>Ivana Kovacova - ivana.kovacova@dell.com')
       



last_run = lr.get_last_run_time_stamp()
now = dt.datetime.utcnow()
dif = (now - last_run)
dif_time = td.format_timedelta(dif)
st.header('')
st.write(f'Last data update: {dif_time} ago')