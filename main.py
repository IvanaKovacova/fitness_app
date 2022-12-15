import streamlit as st
import pandas as pd
from milestone_tab import milestone
from overview_tab import overview
from team_graph_tab import team_graph
from text_tabs import general, faq


st.set_page_config(
    page_title= 'DADS Fitness Challenge', 
    layout="wide", 
    page_icon= ':sports_medal:'
    )

# center the Dell logo in sidebar
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

df = pd.read_excel('data/data_all.xlsx', usecols = ['Name', 'Activity', 'Date'])

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Team Standings','Activities Overview', 'Milestones Achievement', 'FAQ', 'General Information'])

with tab1:  
    team_graph()
    
with tab2:
    overview()
         
with tab3:
    milestone()
    
with tab4:
    faq()
    
with tab5:
    general()     
       
# information about last data in the app
col1, col2, col3 = st.columns(3)
df['Date'] = df['Date'].dt.date
df.sort_values(by = 'Date', ascending = False, inplace=True)
last_data = df.iloc[0]['Date'].strftime('%A %B %d, %Y')

with col3:
    st.header('')
    st.write(f'Newest data are from {last_data}')
