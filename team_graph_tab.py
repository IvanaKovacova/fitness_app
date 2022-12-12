import streamlit as st
import pandas as pd
import plotly.express as px
from comparison_option import comparison

    
def team_graph():
    df = pd.read_excel('data/data_all.xlsx', usecols = ['Name', 'Team', 'Date', 'Total_points_with_bonus'])
    df['Date'] = df['Date'].dt.date
    dic_of_colors = {
        "Fit don't quit": '#0672CB', 
        'Not fast but furious': '#FF99A1', 
        'The Gladeaters':'#5D8C00',
        'Pace Makers': '#66278F',
        'The Pokemons': '#F8A433',
        'Flab-u-less!': '#D0353F',
        'Unstoppable 9': '#9BC438',
        'FANTASTIC 9': '#C47AF4',
        "J's Kaarmaa": '#A64600',
        'No Mo Junk in da Trunk': '#5CC1EE'
        }
    
    data_update_data = pd.read_pickle('data/data_update_data.pkl')
    
    new_activities = (data_update_data.iloc[1,0] - data_update_data.iloc[0,0]).astype('str')
    all_kilometers = data_update_data.iloc[1,1].astype('int').astype('str')
    new_kilometers = (data_update_data.iloc[1,1] - data_update_data.iloc[0,1]).astype('int').astype('str')
    all_hours = (data_update_data.iloc[1,2]/60).astype('int').astype('str')
    new_hours = ((data_update_data.iloc[1,2] - data_update_data.iloc[0,2])/60).astype('int').astype('str')
    
    st.subheader('Overall stats')
    st.write('Please note that despite our best efforts, discrepancies in data may happen.')
    st.write('Each participant is responsible for controlling their own data and reporting discrepancies or missing data to the organizers.')
    left, mid, right = st.columns(3)
    with left:
        st.metric(label ='🏋 Total activities', value=data_update_data.iloc[1,0], delta = new_activities)
    with mid:
        st.metric(label ='🏃 Total kilometers', value= all_kilometers, delta = new_kilometers)
    with right:
        st.metric(label ='🕛 Total hours', value=all_hours, delta = new_hours)
        
    # option 1
    data_points = (
        df
        .groupby('Team')['Total_points_with_bonus']
        .sum()
        .reset_index()
        .sort_values(by = 'Total_points_with_bonus', ascending = False)
        )

    fig_points = (
        px.bar(data_points, 
               x = 'Team', 
               y= 'Total_points_with_bonus', 
               color= 'Team',
               color_discrete_map = dic_of_colors,
               text= 'Total_points_with_bonus',
               title = '<b>Points by Team</b>',
               
               )
        .update_layout(
            title = {
                'x': 0.5
                },
            xaxis_title = '',
            yaxis_title ='Total Team Points',
            template = 'plotly_white',   
            height = 550,
            title_font_size =24
            )
        .update_traces(
            showlegend=False,
            textposition='outside',
            hovertemplate= '%{y:.0f} points',
            texttemplate = '%{y:.0f} pts'
            )
        )
        
    # option 2
    data_evolution = (
        df
        .sort_values(by = 'Date')
        .assign(team_points_cum = lambda x: x.groupby(['Team'])['Total_points_with_bonus'].cumsum())
        )
    fig_evolution = (
        px.line(data_evolution,
                x = 'Date',
                y = 'team_points_cum',
                color = 'Team',
                color_discrete_map = dic_of_colors,
                title = '<b>Evolution of Team Points</b>',
                hover_name = 'Team'
                )
        .update_layout(
            title = {
                'x': 0.5
                },
            xaxis_title = '',
            yaxis_title ='Team points',
            template = 'plotly_white',   
            height = 550,
            title_font_size =24
            )
        .update_traces(
            hovertemplate= '%{x}<br>%{y:.0f} points'
            )
        )
    
        
    
    option = st.selectbox('Choose view', options = ['Points Overview', 'Evolution of Team Points', 'Comparison'])
    if option == 'Points Overview':
        st.plotly_chart(fig_points, use_container_width=True)
    elif option == 'Evolution of Team Points':
        st.plotly_chart(fig_evolution, use_container_width=True)
    elif option == 'Comparison':
        comparison()

    team_df = pd.read_excel('data/teams.xlsx')
    st.table(team_df)