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
        'Total_points_with_bonus': 'Total points w. bonus'
        },
        inplace=True)
    
    # define colors used later in the graphs
    list_of_colors = ['#0672CB', '#FF99A1', '#5D8C00','#C47AF4','#A64600', '#5CC1EE', '#D0353F', '#9BC438', '#66278F', '#F8A433']

    # filtering by date
    def select_date():
        select_date = st.date_input(label = "Choose which day's activities you want to display", 
                                    key = 'select_date',
                                    min_value = dt.date(2022, 12, 10),
                                    max_value = dt.date(2023, 3, 19)
                                    )
        
        if select_date: 
            df_show = df.query('Date == @select_date').reset_index(drop=True)
            st.dataframe(
                data = df_show
                .style.format({'Distance':"{:.1f} km",'Activity Points':"{:.1f}",'Daily Points':"{:.0f}",'Total points w. bonus':"{:.1f}"}),
                width = 1400
                )
    # filtering by team
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
            .groupby(['Name'])['Total points w. bonus']
            .sum()
            .reset_index()
            .sort_values(by = 'Total points w. bonus', ascending = False)
            )
        
        # create graphs next to each other
        left, right = st.columns(2)
        with left:
            fig_member_points = (
                px.pie(data_member,
                       values = 'Total points w. bonus',
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
                    y= 'Total points w. bonus', 
                    color= 'Name',
                    color_discrete_sequence = list_of_colors,
                    text= 'Total points w. bonus'
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
            .style.format({'Distance':"{:.1f} km",'Activity Points':"{:.1f}",'Daily Points':"{:.0f}",'Total points w. bonus':"{:.1f}"}),
            width = 1400
            )
    # filter by name    
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
            .style.format({'Distance':"{:.1f} km",'Activity Points':"{:.1f}",'Daily Points':"{:.0f}",'Total points w. bonus':"{:.1f}"}),
            width = 1400
            )
        # graph of points evolution
        data_evolution = (
            data_name
            .sort_values(by = 'Date')
            .assign(points_cum = lambda x: x.groupby('Name')['Total points w. bonus'].cumsum())
            )
        fig_evolution = (
            px.line(data_evolution,
                    x = 'Date',
                    y = 'points_cum',
                    title = '<b>Evolution of Individual Points</b>',
                    hover_name = 'Date',
                    color_discrete_sequence = list_of_colors
                    )
            .update_layout(
                title = {
                    'x': 0.5
                    },
                xaxis_title = '',
                yaxis_title ='Points',
                template = 'plotly_white',   
                height = 550,
                title_font_size =24
                )
            .update_traces(
                hovertemplate= '%{x}<br>%{y:.0f} points'
                )
            )
        st.plotly_chart(fig_evolution, use_container_width=True)

        
    st.subheader('')
    option = st.selectbox('Choose view', options = ['Show all', 'Filter by Date', 'Filter by Team', 'Filter by Name'])
       
    
    if option == 'Show all':
        st.dataframe(
            data = df.sort_values(by = 'Date', ascending = False).reset_index(drop = True)
            .style.format({'Distance':"{:.1f} km",'Activity Points':"{:.1f}",'Daily Points':"{:.0f}",'Total points w. bonus':"{:.1f}"}),
            width = 1400
            )

    elif option == 'Filter by Date':
        select_date()
    elif option == 'Filter by Team':
        select_team()
    elif option == 'Filter by Name':
        select_name()

        
    st.write('You can sort the table by clicking on column names')

