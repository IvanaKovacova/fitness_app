import pandas as pd
import datetime as dt
import last_run as lr

lr.save_last_run_time_stamp()

# load previous data
df = pd.read_excel('data_all.xlsx', dtype='object')

# Import new data
df_new = pd.read_csv('data_new.csv', usecols = [1, 5, 4, 2, 6, 9], dtype='object')  
df_new.rename(columns= {list(df_new)[0]: 'Activity_ID', list(df_new)[1]: 'Activity'}, inplace = True)
df_new.replace({'E-Bike Ride':'Cycling','Ride':'Cycling', 'Virtual Ride':'Cycling',
                'Virtual Run': 'Run','Trail Run':'Run',
                'Stair-Stepper': 'Walk', 'Hike': 'Walk'}, inplace = True)
df_new.fillna(value = 0, inplace=True)

# get date    
df_new[['Date', 'Time']] = df_new['Date'].str.split(pat ='T', n =1, expand = True)
df_new.drop(columns = 'Time', inplace = True)
df_new['Date'] = pd.to_datetime(df_new['Date'], format="%Y-%m-%d")

# rename other activities
sports = ['Cycling', 'Run', 'Swim', 'Other', 'Walk']
df_new.loc[~df_new['Activity'].isin(sports), 'Activity'] = 'Other' 

# Create df with only new activities
df_diff = df_new[~df_new['Activity_ID'].isin(df['Activity_ID'])].copy()

# prep duration and distance data
# df_diff['Duration'] = pd.to_datetime(df_diff['Duration'])
df_diff['duration_hours'] = pd.to_datetime(df_diff['Duration']).dt.hour
df_diff['duration_minutes'] = pd.to_datetime(df_diff['Duration']).dt.minute
# df_diff.drop(columns = 'Duration', inplace = True)
df_diff['Day_of_week'] = df_diff['Date'].dt.day_name()
df_diff['Distance'] = df_diff['Distance'].astype(str).str.replace(pat = ',', repl = '').astype(float).fillna(value = 0)

# assign activity points by activity
df_diff.loc[df_diff['Activity'].isin(['Walk', 'Run']), 'Activity_points'] = df_diff['Distance']*5
df_diff.loc[df_diff['Activity'] == 'Cycling', 'Activity_points'] = df_diff['Distance']
df_diff.loc[df_diff['Activity'] == 'Swim', 'Activity_points'] = df_diff['Distance']/100*4
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] >=2), 'Activity_points'] = 40
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] ==1) & (df_diff['duration_minutes'] >= 30), 'Activity_points'] = 30
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] ==1) & (df_diff['duration_minutes'] < 30), 'Activity_points'] = 20
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] ==0) & (df_diff['duration_minutes'] >= 30), 'Activity_points'] = 10
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] ==0) & (df_diff['duration_minutes'] < 30), 'Activity_points'] = 0

# Check length of old data
old_len = len(df)

# concat old & new data
df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")
df = (
    pd
    .concat([df,df_diff])
    .sort_values(by = ['Date', 'Name'], ignore_index = True)
    .query('Date >= "2022-08-01"')
#    .query('Date <= "2022-11-20"') #replace later
)

# choose top 2 activities for each person
df_top2 = (
    df
    .sort_values('Activity_points', ascending = False)
    .groupby(['Date', 'Name'])
    .head(2)
    .sort_values(['Date', 'Name'], ascending = False, ignore_index = True)
)

# assign 20 daily points to one daily activity per person & 0 to the rest
with_daily_points = (
    df_top2
    .sort_values('Activity_points', ascending = False)
    .groupby(['Date', 'Name'])
    .head(1)
    .sort_values(['Date', 'Name'], ascending = False, ignore_index = True)
    .assign(Daily_points = 20)
)

no_daily_points = (
    df_top2[~df_top2['Activity_ID'].isin(with_daily_points['Activity_ID'])]
    .copy()
    .assign(Daily_points = 0)
    .sort_values(['Date', 'Name'], ascending = False, ignore_index = True)
)

# points without 2x and 3x
df_points = (
    pd
    .concat([with_daily_points, no_daily_points])
    .sort_values(['Date', 'Name'], ascending = False, ignore_index = True)
    .assign(Total_points = lambda x: x.Activity_points + x.Daily_points)
)

# create column marking 2X and 3X days
# default value
df_points['Bonus'] = 'None'

# 2X
df_points.loc[(df_points['Day_of_week'] == 'Saturday') | (df_points['Day_of_week'] == 'Sunday'), 'Bonus'] = '2X'

# 3X
triple_x_list = ['2022-11-17T00:00:00.000000000', '2022-11-21T00:00:00.000000000']
df_points.loc[df_points['Date'].isin(triple_x_list), 'Bonus'] = '3X'

# create calculation of days between activities for the great comeback award
# time difference between rows of one person
df_points.sort_values(['Name','Date'], inplace = True, ignore_index = True)
df_points['Difference'] = df_points.groupby('Name')['Date'].diff().fillna(pd.Timedelta('0 days')).dt.days
df_points.loc[df_points['Difference'] >= 14, 'Comeback'] = True
df_points.loc[df_points['Difference'] < 14, 'Comeback'] = False

# add the extra points for final points
# basic value
df_points['Total_points_with_bonus'] = df_points['Total_points']

# 2X Saturdays and Sundays
df_points.loc[df_points['Bonus'] == '2X', 'Total_points_with_bonus'] = df_points['Total_points']*2

# 3X based on a list (replace dates)
df_points.loc[df_points['Bonus'] == '3X', 'Total_points_with_bonus'] = df_points['Total_points']*3

# great comeback
df_points.loc[df_points['Comeback'] == True, 'Total_points_with_bonus'] = df_points['Total_points'] + 100

# check length of new df against old df
new_len = len(df_points)
print(f'Old df length = {old_len}')
print(f'New df length = {new_len}')

# export data to excel
df_points.to_excel('data_all.xlsx', index=False)