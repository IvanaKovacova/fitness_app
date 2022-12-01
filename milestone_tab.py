import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

def milestone():
    df = pd.read_excel('data/data_all.xlsx', usecols = ['Name', 'Activity', 'Date', 'Distance', 'Duration', 'Activity_points', 'Daily_points', 'Bonus', 'Total_points_with_bonus'])
    df['Date'] = df['Date'].dt.date
    
    st.subheader('Milestone awards fulfillment')        

    cycling = (
        df
        .query('Activity == "Cycling"')
        .copy()
        .groupby('Name')['Distance']
        .sum()
        .reset_index()
        .assign(limit = lambda x: np.where(x['Distance'] >= 1000, 'yes', 'no'))
        .sort_values(by = 'Distance', ascending = False)
        )
    fig = (
        px.bar(cycling,
               x = 'Name', 
               y='Distance', 
               title = '<b>1000 km Cycling Award</b>', 
               text ='Distance', 
               color = 'limit',
               color_discrete_map={"yes": '#0672CB', "no": '#FF99A1'}
              )
        .update_layout(
            title_font_size =24,
            xaxis_title= ' ',
            yaxis_title = 'Kilometers',
            title_x = 0.5,
            template = 'plotly_white',
            height = 600
        )
        .update_traces(
            texttemplate = '%{text:.1f} km',
            textposition = 'outside',
            hovertemplate= '%{x}<br>%{y:.1f} km',
            showlegend=False
        )
        .add_hline(y=1000, line_width = 4, line_color = '#FE6873')
    )
    
    run_walk = (
        df
        .query('Activity == "Run" | Activity == "Walk"')
        .copy()
        .groupby('Name')['Distance']
        .sum()
        .reset_index()
        .assign(limit = lambda x: np.where(x['Distance'] >= 200, 'yes', 'no'))
        .sort_values(by = 'Distance', ascending = False)
        )
    fig2 = (
        px.bar(run_walk,
               x = 'Name', 
               y='Distance', 
               title = '<b>200 km of Running/Walking award</b>', 
               text ='Distance', 
               color = 'limit',
               color_discrete_map={"yes": '#0672CB', "no": '#FF99A1'}
              )
        .update_layout(
            title_font_size =24,
            xaxis_title= ' ',
            yaxis_title = 'Kilometers',
            title_x = 0.5,
            template = 'plotly_white',
            height = 600,
            width = 1000
        )
        .update_traces(
            texttemplate = '%{text:.1f} km',
            textposition = 'outside',
            hovertemplate= '%{x}<br>%{y:.1f} km',
            showlegend=False
        )
        .add_hline(y=200, line_width = 4, line_color = '#FE6873')
    )
    
    swim = (
        df
        .query('Activity == "Swim"')
        .copy()
        .groupby('Name')['Distance']
        .sum()
        .reset_index()
        .assign(limit = lambda x: np.where(x['Distance'] >= 25, 'yes', 'no'))
        .sort_values(by = 'Distance', ascending = False)
        )
    fig3 = (
        px.bar(swim,
               x = 'Name', 
               y='Distance', 
               title = '<b>25 km of Swimming Award</b>', 
               text ='Distance', 
               color = 'limit',
               color_discrete_map={"yes": '#0672CB', "no": '#FF99A1'}
              )
        .update_layout(
            title_font_size =24,
            xaxis_title= ' ',
            yaxis_title = 'Kilometers',
            title_x = 0.5,
            template = 'plotly_white',
            height = 600,
            width = 1000
        )
        .update_traces(
            texttemplate = '%{text:.1f} km',
            textposition = 'outside',
            hovertemplate= '%{x}<br>%{y:.1f} km',
            showlegend=False
        )
        .add_hline(y=25, line_width = 4, line_color = '#FE6873')
    )
    
    other = (
        df
        .query('Activity == "Other"')
        .copy()
        .groupby('Name')['Activity']
        .count()
        .reset_index()
        .assign(limit = lambda x: np.where(x['Activity'] >= 20, 'yes', 'no'))
        .sort_values(by = 'Activity', ascending = False)
        )
    fig4 = (
        px.bar(other,
               x = 'Name', 
               y='Activity', 
               title = '<b>Versatility award for 20 other activities</b>', 
               text ='Activity', 
               color = 'limit',
               color_discrete_map={"yes": '#0672CB', "no": '#FF99A1'}
              )
        .update_layout(
            title_font_size =24,
            xaxis_title= ' ',
            yaxis_title = 'Number of other activities by person',
            title_x = 0.5,
            template = 'plotly_white',
            height = 600,
            width = 1000
        )
        .update_traces(
            texttemplate = '%{text:.0f} activities',
            textposition = 'outside',
            hovertemplate= '%{x}<br>%{y} activities',
            showlegend=False
        )
        .add_hline(y=20, line_width = 4, line_color = '#FE6873')
    )
    
    #comeback
    df_comeback = (
        pd
        .read_excel('data/data_all.xlsx', usecols = ['Name', 'Team', 'Activity', 'Duration', 'Distance', 'Date', 'Comeback', 'Difference'])
        .rename(columns = {'Difference' : 'Inactivity Duration'})
        .query('Comeback == True')
        .sort_values('Date', ascending=False)
        )
    df_comeback['Date'] = df_comeback['Date'].dt.date
    
    option = st.selectbox('Choose award which you want to check', options = ['Cycling', 'Swimming', 'Running/Walking', 'Other', 'Great Comeback Award'])
    if option == 'Cycling':
        st.plotly_chart(fig, use_container_width=True)
    elif option == 'Swimming':
        st.plotly_chart(fig3, use_container_width=True)
    elif option == 'Running/Walking':
        st.plotly_chart(fig2, use_container_width=True)
    elif option == 'Other':
        st.plotly_chart(fig4, use_container_width=True)
    elif option == 'Great Comeback Award':
        st.subheader('Check who returned after inactivity of at least 14 days')
        st.dataframe(data =df_comeback[['Name', 'Team', 'Activity', 'Duration', 'Distance', 'Date', 'Inactivity Duration']]
                     .style.format({'Distance':"{:.1f} km"}),
                     width= 1400)