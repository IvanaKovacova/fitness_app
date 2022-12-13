import streamlit as st
import pandas as pd
import plotly.express as px
from comparison_option import comparison

    
def team_graph():
    df = pd.read_excel('data/data_all.xlsx', usecols = ['Name', 'Team','Distance', 'Date', 'duration_hours', 'duration_minutes', 'Total_points_with_bonus'])
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
    
#    data_update_data = pd.read_pickle('data/data_update_data.pkl')
    
    total_length = len(df)
    df.sort_values(by = 'Date', ascending = False, inplace = True)
    yesterday = df.iloc[0]['Date']
    new_length = len(df.loc[df['Date'] == yesterday])
    total_kms = df['Distance'].astype('int64').sum().astype('str')
    new_kilometers = df['Distance'].astype('int64').loc[df['Date'] == yesterday].sum().astype('str')

    all_mins = (df['duration_hours'].astype('int64').sum())*60 + df['duration_minutes'].astype('int64').sum()
    all_hours = (all_mins/60).astype('int').astype('str')
    df_new_hours = df.query('Date == @yesterday')
    new_hours = (((df_new_hours['duration_hours'].astype('int64').sum())*60 + df_new_hours['duration_minutes'].astype('int64').sum())/60).astype('int64').astype('str')
    
    st.subheader('Overall stats')
    st.write('Please note that despite our best efforts, discrepancies in data may happen.')
    st.write('Each participant can help us by checking their activities and reporting discrepancies or missing data to the organizers.')
    st.write('')
    left, mid, right = st.columns(3)
    with left:
        st.metric(label ='🏋 Total activities', value=total_length, delta = new_length)
    with mid:
        st.metric(label ='🏃 Total kilometers', value= total_kms, delta = new_kilometers)
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