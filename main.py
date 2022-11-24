import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import datetime as dt
import last_run as lr


st.set_page_config(layout="wide")

df = pd.read_excel('data_all.xlsx', usecols = ['Name', 'Activity', 'Date', 'Distance', 'Duration', 'Activity_points', 'Daily_points', 'Bonus', 'Total_points_with_bonus'])
df['Date'] = df['Date'].dt.date
df.loc[df['Activity'] == 'Swim', 'Distance'] = df['Distance']/1000


tab1, tab2, tab3 = st.tabs(['Graphs', 'Table', 'Milestones'])

    
with tab1:
    st.header('Graphs')
    st.subheader('See your points in graphs')
    
    left, mid = st.columns(2)
    
    name = left.multiselect(
        'Name',
        options=df['Name'].unique(),
        default = df['Name'].unique(),
        )

    activity = mid.multiselect(
        'Activity',
        options = df['Activity'].unique(),
        default = df['Activity'].unique()
        )
    
    df_show = (
        df
        .query("Name == @name & Activity == @activity")
        .groupby(['Name', 'Activity'])['Total_points_with_bonus'].sum()
        .reset_index()
        .sort_values(by = 'Total_points_with_bonus', ascending = False)
        )
        
    fig_comparison = (
        px.bar(df_show, 
               x = 'Name', 
               y= 'Total_points_with_bonus', 
               color= 'Activity'
               )
        .update_layout(
            xaxis_title = '',
            yaxis_title ='Points by activity',
            template = 'plotly_white'
            )
        )
    
    st.plotly_chart(fig_comparison, use_container_width=True)
    
with tab2:  
    st.header('Table')
    st.subheader('Review all activities up to date.')
    st.write('You can sort the table by clicking on column names')
    
    st.dataframe(
        data = df
        .style.format({'Distance':"{:.1f} km",'Activity_points':"{:.1f}",'Daily_points':"{:.0f}",'Total_points_with_bonus':"{:.1f}"}),
        width = 1000
        )
    
with tab3:
    st.header('Milestone awards fulfillment')
    
    
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
               title = 'Cycling award for 1000kms of riding', 
               text ='Distance', 
               color = 'limit',
               color_discrete_map={"yes": '#EF553B', "no": '#636EFA'}
              )
        .update_layout(
            xaxis_title= ' ',
            yaxis_title = 'Kilometers',
            title_x = 0.5,
            template = 'plotly_white',
            height = 600
        )
        .update_traces(
            texttemplate = '%{text:.1f} kms',
            textposition = 'outside'
        )
        .add_hline(y=1000)
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
               title = 'Running/walking award for 200 kms of running/walking', 
               text ='Distance', 
               color = 'limit',
               color_discrete_map={"yes": '#EF553B', "no": '#636EFA'}
              )
        .update_layout(
            xaxis_title= ' ',
            yaxis_title = 'Kilometers',
            title_x = 0.5,
            template = 'plotly_white',
            height = 600,
            width = 1000
        )
        .update_traces(
            texttemplate = '%{text:.1f} kms',
            textposition = 'outside'
        )
        .add_hline(y=200)
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
               title = 'Swimming award for swimming 25 kms', 
               text ='Distance', 
               color = 'limit',
               color_discrete_map={"yes": '#EF553B', "no": '#636EFA'}
              )
        .update_layout(
            xaxis_title= ' ',
            yaxis_title = 'Kilometers',
            title_x = 0.5,
            template = 'plotly_white',
            height = 600,
            width = 1000
        )
        .update_traces(
            texttemplate = '%{text:.1f} kms',
            textposition = 'outside'
        )
        .add_hline(y=25)
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
               title = 'Versatility award for 20 other activities', 
               text ='Activity', 
               color = 'limit',
               color_discrete_map={"yes": '#EF553B', "no": '#636EFA'}
              )
        .update_layout(
            xaxis_title= ' ',
            yaxis_title = 'Number of other activities by person',
            title_x = 0.5,
            template = 'plotly_white',
            height = 600,
            width = 1000
        )
        .update_traces(
            texttemplate = '%{text:.0f} activities',
            textposition = 'outside'
        )
        .add_hline(y=20)
    )
    
    option = st.selectbox('Choose award which you want to check', options = ['Cycling', 'Swimming', 'Running/Walking', 'Other'])
    if option == 'Cycling':
        st.plotly_chart(fig, use_container_width=True)
    elif option == 'Swimming':
        st.plotly_chart(fig3, use_container_width=True)
    elif option == 'Running/Walking':
        st.plotly_chart(fig2, use_container_width=True)
    elif option == 'Other':
        st.plotly_chart(fig4, use_container_width=True)

last_run = lr.get_last_run_time_stamp()
st.write(f'Last data update: {last_run}')