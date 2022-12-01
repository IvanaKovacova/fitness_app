import streamlit as st
import pandas as pd
import plotly.express as px

def comparison():
    df = pd.read_excel('data/data_all.xlsx')
    df['Date'] = df['Date'].dt.date
    
    # prepare graphs
    left, mid = st.columns(2)
    
    team = left.multiselect(
        'Team',
        options = df['Team'].unique(),
        default = df['Team'].unique()
        )
  

    activity = mid.multiselect(
        'Activity',
        options = df['Activity'].unique(),
        default = df['Activity'].unique()
        )
    
    name = st.multiselect(
        'Name',
        options=df['Name'].unique(),
        default = df['Name'].unique()
        )
    
    list_of_colors = ['#0672CB','#5D8C00','#66278F','#F8A433','#FE6873']

    df_sum = (
        df
        .query("Team == @team & Name == @name & Activity == @activity")
        .groupby('Name')['Total_points_with_bonus'].sum()
        .reset_index()
        .sort_values(by = 'Total_points_with_bonus', ascending = False)
        )
    
    fig_comparison_total_points = (
        px.bar(df_sum, 
               x = 'Name', 
               y= 'Total_points_with_bonus', 
               color_discrete_sequence= list_of_colors,
               color = 'Name',
               title = 'Total points',
               text = 'Total_points_with_bonus'
               )
        .update_layout(
            showlegend=False,
            title = {
                'x': 0.5
                },
            title_font_size = 24,
            xaxis_title = '',
            yaxis_title ='Points',
            template = 'plotly_white',
            height = 600
            )
        .update_traces(
            hovertemplate= '%{y:.0f} points',
            texttemplate = '%{y:.0f} pts',
            textposition = 'outside'
            )
        )
    
    df_show = (
        df
        .query("Team == @team & Name == @name & Activity == @activity")
        .groupby(['Name', 'Activity'])['Total_points_with_bonus'].sum()
        .reset_index()
        .sort_values(by = 'Total_points_with_bonus', ascending = False)
        )
        
    fig_comparison_points = (
        px.bar(df_show, 
               x = 'Name', 
               y= 'Total_points_with_bonus', 
               color= 'Activity',
               color_discrete_map={
                   "Swim": '#0672CB',
                   "Cycling": '#5D8C00',
                   'Run': '#66278F',
                   'Walk': '#F8A433',
                   'Other': '#FE6873'
                   },
               title = 'Points by activity'
               )
        .update_layout(
            title = {
                'x': 0.5
                },
            title_font_size = 24,
            xaxis_title = '',
            yaxis_title ='Points by activity',
            template = 'plotly_white',
            height = 600
            )
        .update_traces(
            hovertemplate= '%{x}<br>%{y:.0f} points'
            )
        )

    
    df_time = (
        df
        .query("Team == @team & Name == @name & Activity == @activity")
        .assign(total_time_in_minutes = lambda x: x['duration_hours']*60 + x['duration_minutes'])
        .groupby(['Name', 'Activity'])['total_time_in_minutes'].sum()
        .reset_index()
        .sort_values(by = 'total_time_in_minutes', ascending = False)
        )
        
    fig_comparison_time = (
        px.bar(df_time, 
               x = 'Name', 
               y= 'total_time_in_minutes', 
               color= 'Activity',
               color_discrete_map={
                   "Swim": '#0672CB',
                   "Cycling": '#5D8C00',
                   'Run': '#66278F',
                   'Walk': '#F8A433',
                   'Other': '#FE6873'
                   },
               title = 'Comparison by duration in minutes'
               )
        .update_layout(
            title = {
                'x': 0.5
                },
            title_font_size = 24,
            xaxis_title = '',
            yaxis_title ='Duration by activity',
            template = 'plotly_white'
            )
        .update_traces(
            hovertemplate= '%{x}<br>%{y} min'
            )
        )
    
    
    df_distance = (
        df
        .query("Team == @team & Name == @name & Activity == @activity")
        .groupby(['Name', 'Activity'])['Distance'].sum()
        .reset_index()
        .sort_values(by = 'Distance', ascending = False)
        )
        
    fig_comparison_distance = (
        px.bar(df_distance, 
               x = 'Name', 
               y= 'Distance', 
               color= 'Activity',
               color_discrete_map={
                   "Swim": '#0672CB',
                   "Cycling": '#5D8C00',
                   'Run': '#66278F',
                   'Walk': '#F8A433',
                   'Other': '#FE6873'
                   },
               title = 'Comparison by distance'
               )
        .update_layout(
            title = {
                'x': 0.5
                },
            title_font_size = 24,
            xaxis_title = '',
            yaxis_title ='Distance by activity',
            template = 'plotly_white'
            )
        .update_traces(
            hovertemplate= '%{x}<br>%{y:.0f} km'
            )
        )

# page output
    
    
    type_of_graph = st.selectbox('Select which metric you want to compare', options=['Points', 'Duration', 'Distance'])


    if type_of_graph == 'Points':
        st.plotly_chart(fig_comparison_total_points, use_container_width=True)
        st.plotly_chart(fig_comparison_points, use_container_width=True)
    elif type_of_graph == 'Duration':
        st.plotly_chart(fig_comparison_time, use_container_width=True)
    elif type_of_graph == 'Distance':
        st.plotly_chart(fig_comparison_distance, use_container_width=True)
