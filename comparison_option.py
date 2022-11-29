import streamlit as st
import pandas as pd
import plotly.express as px

def comparison():
    st.subheader('Check the graphs to see your progress')
    
    df = pd.read_excel('data/data_all.xlsx', usecols = ['Name', 'Team', 'Activity', 'Date', 'Distance', 'Duration', 'Activity_points', 'Daily_points', 'Bonus', 'Total_points_with_bonus'])
    df['Date'] = df['Date'].dt.date
    
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

   
    df_show = (
        df
        .query("Team == @team & Name == @name & Activity == @activity")
        .groupby(['Name', 'Activity'])['Total_points_with_bonus'].sum()
        .reset_index()
        .sort_values(by = 'Total_points_with_bonus', ascending = False)
        )
        
    fig_comparison = (
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
                   }
               )
        .update_layout(
            xaxis_title = '',
            yaxis_title ='Points by activity',
            template = 'plotly_white'
            )
        .update_traces(
            hovertemplate= '%{x}<br>%{y} points'
            )
        )
    
    st.plotly_chart(fig_comparison, use_container_width=True)

    