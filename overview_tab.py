import pandas as pd
import streamlit as st
import datetime as dt
import plotly.express as px

def overview():
    df = pd.read_excel('data/data_all.xlsx', usecols = ['Name', 'Team', 'Activity', 'Date', 'Distance', 'Duration', 'Activity_points', 'Daily_points', 'Bonus', 'Total_points_with_bonus'])
    df['Date'] = df['Date'].dt.date
    df.rename(columns={
        'Activity_points':'Activity Points',
        'Daily_points': 'Daily Points',
        'Total_points_with_bonus': 'Total points including bonus'
        }, inplace=True)
    
    list_of_colors = ['#0672CB', '#FF99A1', '#5D8C00','#A8396F', '#F8A433', '#B85200','#DB9EFF', '#8C161F', '#FEC97A', '#66278F', '#FE6873']

   
    
    def select_date():
        select_date = st.date_input(label = "Choose which day's activities you want to display (defaults to today)", key = 'select_date')
        
        if select_date: 
            df_show = df.query('Date == @select_date').reset_index(drop=True)
            st.dataframe(
                data = df_show
                .style.format({'Distance':"{:.1f} km",'Activity Points':"{:.1f}",'Daily Points':"{:.0f}",'Total points including bonus':"{:.1f}"}),
                width = 1400
                )
    
    def select_team():
        select_team = st.selectbox(
            'Choose team', 
            options = df['Team'].unique()
            )
        st.subheader('')

        data_team = (
            df
            .query('Team == @select_team')
            .sort_values(by = 'Date', ascending = False)
            .reset_index(drop=True)
            )

        data_member = (
            data_team
            .groupby(['Name'])['Total points including bonus']
            .sum()
            .reset_index()
            .sort_values(by = 'Total points including bonus', ascending = False)
            )
        left, right = st.columns(2)
        with left:
            fig_member_points = (
                px.pie(data_member,
                       values = 'Total points including bonus',
                       names = 'Name',
                       color_discrete_sequence = list_of_colors
                       )
                .update_traces(
                    showlegend=False,
                    textposition = 'outside',
                    texttemplate= "%{label}<br>%{percent:.1%}",
                    selector=dict(type='pie'),
                    hovertemplate = "%{value:.0f} points"
                    )
                )
            st.plotly_chart(fig_member_points, use_container_width=True)
        with right:
            fig_member_points2 = (
                px.bar(
                    data_member,
                    x = 'Name', 
                    y= 'Total points including bonus', 
                    color= 'Name',
                    color_discrete_sequence = list_of_colors,
                    text= 'Total points including bonus'
                    )
             .update_layout(
                 xaxis_title = '',
                 yaxis_title ='Points by Person',
                 template = 'plotly_white',   
                 )
             .update_traces(
                 showlegend=False,
                 textposition='outside',
                 hovertemplate= '%{y:.0f} points',
                 texttemplate = '%{y:.0f} pts'
                 )
             )
            st.plotly_chart(fig_member_points2, use_container_width=True)
            
        st.subheader('')

        st.dataframe(
            data = data_team
            .style.format({'Distance':"{:.1f} km",'Activity Points':"{:.1f}",'Daily Points':"{:.0f}",'Total points including bonus':"{:.1f}"}),
            width = 1400
            )
        
    def select_name():
        select_name = st.selectbox(
            'Choose name', 
            options = df['Name'].unique()
            )
        st.subheader('')

        data_name = (
            df
            .query('Name == @select_name')
            .sort_values(by = 'Date', ascending = False)
            .reset_index(drop = True)
            )
        st.dataframe(
            data = data_name
            .style.format({'Distance':"{:.1f} km",'Activity Points':"{:.1f}",'Daily Points':"{:.0f}",'Total points including bonus':"{:.1f}"}),
            width = 1400
            )
        
        
    st.subheader('')
    option = st.selectbox('Choose view', options = ['Show all', 'Filter by Date', 'Filter by Team', 'Filter by Name'])
       
    
    if option == 'Show all':
        st.dataframe(
            data = df.sort_values(by = 'Date', ascending = False).reset_index(drop = True)
            .style.format({'Distance':"{:.1f} km",'Activity Points':"{:.1f}",'Daily Points':"{:.0f}",'Total points including bonus':"{:.1f}"}),
            width = 1400
            )
    elif option == 'Filter by Date':
        select_date()
    elif option == 'Filter by Team':
        select_team()
    elif option == 'Filter by Name':
        select_name()

        
    st.write('You can sort the table by clicking on column names')

