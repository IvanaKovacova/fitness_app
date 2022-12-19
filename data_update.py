import pandas as pd
import datetime as dt


# load previous data
df = pd.read_excel('data/data_all.xlsx', dtype='object')
df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d")

# Import new data
df_new = pd.read_csv('data/data_new.csv', usecols = [1, 5, 4, 2, 6, 9, 3], dtype='object')  
df_new.rename(columns= {list(df_new)[0]: 'Activity_ID', list(df_new)[1]: 'Activity'}, inplace = True)
df_new.replace({'E-Bike Ride':'Cycling','Ride':'Cycling', 'Handcycle': 'Cycling', 'Virtual Ride':'Cycling','Virtual Run': 'Run','Trail Run':'Run','Stair-Stepper': 'Walk', 'Hike': 'Walk'}, inplace = True)
df_new.loc[(df_new['Activity'] == 'unknown') & (df_new['Location'].str.contains('walk', case = False)), 'Activity']  = 'Walk'
df_new.loc[(df_new['Activity'] == 'unknown') & (df_new['Location'].str.contains('hike', case = False)), 'Activity']  = 'Walk'
df_new.loc[(df_new['Activity'] == 'unknown') & (df_new['Location'].str.contains('swim', case = False)), 'Activity']  = 'Swim'
df_new.loc[(df_new['Activity'] == 'unknown') & (df_new['Location'].str.contains('run', case = False)), 'Activity']  = 'Run'
df_new.loc[(df_new['Activity'] == 'unknown') & (df_new['Location'].str.contains('ride', case = False)), 'Activity']  = 'Cycling'
df_new.fillna(value = 0, inplace=True)

# get date    
df_new[['Date', 'Time']] = df_new['Date'].str.split(pat ='T', n =1, expand = True)
df_new.drop(columns = 'Time', inplace = True)
df_new['Date'] = pd.to_datetime(df_new['Date']).dt.normalize()


# rename other activities
sports = ['Cycling', 'Run', 'Swim', 'Other', 'Walk']
df_new.loc[~df_new['Activity'].isin(sports), 'Activity'] = 'Other' 
df_new.loc[df_new['Distance'] == 0, 'Activity'] = 'Other'
df_new['activity_for_points'] = df_new['Activity']
df_new.loc[(df_new['Activity'] == 'Run') | (df_new['Activity'] == 'Walk'), 'activity_for_points'] = 'Run/Walk'

# Create df with only new activities
df_diff = df_new[~df_new['Activity_ID'].isin(df['Activity_ID'])].copy()

# prep duration and distance data
df_diff['duration_hours'] = pd.to_datetime(df_diff['Duration']).dt.hour
df_diff['duration_minutes'] = pd.to_datetime(df_diff['Duration']).dt.minute
df_diff['Day_of_week'] = df_diff['Date'].dt.day_name()
df_diff['Distance'] = df_diff['Distance'].astype(str).str.replace(pat = ',', repl = '').astype(float).fillna(value = 0)
df_diff.loc[df_diff['Activity'] == 'Swim', 'Distance'] = df_diff['Distance']/1000

# assign activity points by activity
df_diff.loc[df_diff['Activity'].isin(['Walk', 'Run']), 'Activity_points'] = df_diff['Distance']*5
df_diff.loc[df_diff['Activity'] == 'Cycling', 'Activity_points'] = df_diff['Distance']
df_diff.loc[df_diff['Activity'] == 'Swim', 'Activity_points'] = df_diff['Distance']*40
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] >=2), 'Activity_points'] = 40
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] ==1) & (df_diff['duration_minutes'] >= 30), 'Activity_points'] = 30
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] ==1) & (df_diff['duration_minutes'] < 30), 'Activity_points'] = 20
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] ==0) & (df_diff['duration_minutes'] >= 30), 'Activity_points'] = 10
df_diff.loc[(df_diff['Activity'] == 'Other') & (df_diff['duration_hours'] ==0) & (df_diff['duration_minutes'] < 30), 'Activity_points'] = 0

# concat old & new data
this_day = dt.date.today()
df = (
    pd
    .concat([df,df_diff])
    .sort_values(by = ['Date', 'Name'], ignore_index = True)
    .query('Date >= "2022-12-10"')
    .query('Date < @this_day') 
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
triple_x_list = ['2022-12-10T00:00:00.000000000', '2023-01-01T00:00:00.000000000', '2023-01-02T00:00:00.000000000', '2023-01-03T00:00:00.000000000', '2023-03-19T00:00:00.000000000']
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
df_points.loc[df_points['Comeback'] == True, 'Total_points_with_bonus'] = (df_points['Total_points_with_bonus'] + 100)
df_points.loc[(df_points['Comeback'] == True) & (df_points['Bonus'] =='2X'), 'Bonus'] = '2X and Comeback'
df_points.loc[(df_points['Comeback'] == True) & (df_points['Bonus'] =='3X'), 'Bonus'] = '3X and Comeback'

# milestones
df_points['Distance'] = df_points['Distance'].astype('float')
df_points['Sum_of_kms'] = df_points.sort_values(by ='Date').groupby(['Name', 'activity_for_points'])['Distance'].transform('cumsum')
df_points['count_of_activities'] = df_points.sort_values(by = 'Date').groupby(['Name', 'activity_for_points'])['Duration'].transform('cumcount')
df_points = df_points.sort_values(by =['Name', 'activity_for_points', 'count_of_activities'])
df_points['previous_km_sum'] = df_points.groupby(['Name', 'activity_for_points'])['Sum_of_kms'].transform(lambda x: x.shift()).fillna(0)

df_points['Milestone'] = False
df_points.loc[(df_points['activity_for_points'] == 'Run/Walk') & (df_points['previous_km_sum'] < 200) & (df_points['Sum_of_kms'] >= 200), 'Milestone'] = True
df_points.loc[(df_points['activity_for_points'] == 'Swim') & (df_points['previous_km_sum'] < 25) & (df_points['Sum_of_kms'] >= 25), 'Milestone'] = True
df_points.loc[(df_points['activity_for_points'] == 'Cycling') & (df_points['previous_km_sum'] < 1000) & (df_points['Sum_of_kms'] >= 1000), 'Milestone'] = True
df_points.loc[(df_points['activity_for_points'] == 'Other') & (df_points['count_of_activities'] == 19), 'Milestone'] = True

df_points.loc[(df_points['Milestone'] == True), 'Bonus'] = 'Milestone'
df_points.loc[(df_points['Milestone'] == True) & ((df_points['Day_of_week'] == 'Saturday') | (df_points['Day_of_week'] == 'Sunday')), 'Bonus'] = '2X and Milestone'
df_points.loc[(df_points['Milestone'] == True) & df_points['Date'].isin(triple_x_list), 'Bonus'] = '3X and Milestone'
df_points.loc[(df_points['Milestone'] == True) & ((df_points['Day_of_week'] == 'Saturday') | (df_points['Day_of_week'] == 'Sunday')) & (df_points['Comeback'] == True), 'Bonus'] = '2X, Milestone, Comeback'
df_points.loc[(df_points['Milestone'] == True) & df_points['Date'].isin(triple_x_list) & (df_points['Comeback'] == True), 'Bonus'] = '3X, Milestone, Comeback'

df_points.loc[(df_points['Milestone'] == True) & (df_points['activity_for_points'] != 'Other'), 'Total_points_with_bonus'] = df_points['Total_points_with_bonus'] +1000
df_points.loc[(df_points['Milestone'] == True) & (df_points['activity_for_points'] == 'Other'), 'Total_points_with_bonus'] = df_points['Total_points_with_bonus'] +500

# specify teams
team_1 = ['Fernanda Mattei', 'Karthik Gunda', 'Tinku Sand', 'Manish Shetty', 'Abhishek Singh', 'Dio Goldoni', 'Krushi Punyamantula', 'Prerna Dewale', 'Victor Caetano']
team_2 = ['Jesse Williams', 'Manoj M','Antônio Ravazzolo', 'Aditya Aggarwal', 'Anjana Prem Kumar', 'Aswani Gande', 'Kunjal Gosar', 'Rafael Fraga Mohr', 'Sravan Katepalli']
team_3 = ['Madhav Parashar', 'Fabia Zarballa', 'Vaibhav Chandan', 'Anvesh Kalia', 'Aarzoo Tandon', 'Ashwini Maddala', 'Leela Krishna', 'Rahul Roy Choudhury', 'Simon Talapa']
team_4 = ['Andrew Cd', 'Brian Fitzgerald', 'Sowjanya Sowji', 'Craig Friedman', 'Aditi Bhardya', 'Balaji Venkatesh', 'Felipe Garcez', 'Rajat Sadanand', 'Suparna Lala']
team_5 = ['Virendra Singh', 'Damien Lorigan', 'Ivana Kovacova', 'Sandeep Patil', 'Ali Mehrnezhad', 'Divya Tallur', 'Marco Martins', 'Ravinder Singh Bisht', 'Tejaswini Sira']
team_6 = ['Shailesh Abecedarian', 'Subramita Dash', 'Aastha Banda', 'Sumit Wadhwa', 'Allen Mills', 'Elena Teytelman', 'Isha Kanani', 'Renoy Zachariah', 'Tushar Bhandari']
team_7 = ['Manimegalai Kailash', 'Sanjay K', 'Jose Martinez', 'Jason Lee', 'Abhishek Sharma', 'Emily Tibbens', 'Nealie Glasser', 'S Santhoshraghavan', 'Sree Kothapalli']
team_8 = ['Prabal Paul', 'Khushboo Mehrotra', 'Enzo Bertoldi', 'Uttam Ghosh', 'Ankit Agarwal', 'Enoch Jolaoso', 'Neha Arora', 'Saranraj Sp', 'Yesrat Rahman']
team_9 = ['Sandeep Malhotra', 'Satish Patil', 'Juraj Mečír', 'Sathyanarayanan Ragothaman', 'Ankit Talele', 'Joyce Miyazato', 'Nikhitha Vegi', 'Shreeja Verma', 'William Matheson']
team_10 = ['Som Shubham Sahoo', 'Preetha Dandapani', 'Jonathon Klanderman', 'Anoop Karunakaran', 'Aruna  N', 'Kalaiselvi Sekar', 'Palak Agarwal', 'Siddharth Malani', 'Victor Frank']

# assign teams
df_points['Name'] = df_points['Name'].str.title()
df_points['Team'] ='Waiting Room'
df_points.loc[df_points['Name'].str.title().isin(team_1), 'Team'] = 'Pace Makers'
df_points.loc[df_points['Name'].str.title().isin(team_2), 'Team'] = "J's Kaarmaa"
df_points.loc[df_points['Name'].str.title().isin(team_3), 'Team'] = 'The Gladeaters'
df_points.loc[df_points['Name'].str.title().isin(team_4), 'Team'] = 'Flab-u-less!'
df_points.loc[df_points['Name'].str.title().isin(team_5), 'Team'] = 'Unstoppable 9'
df_points.loc[df_points['Name'].str.title().isin(team_6), 'Team'] = 'Not fast but furious'
df_points.loc[df_points['Name'].str.title().isin(team_7), 'Team'] = 'The Pokemons'
df_points.loc[df_points['Name'].str.title().isin(team_8), 'Team'] = 'FANTASTIC 9'
df_points.loc[df_points['Name'].str.title().isin(team_9), 'Team'] = "Fit don't Quit"
df_points.loc[df_points['Name'].str.title().isin(team_10), 'Team'] = 'No Mo Junk in da Trunk'

df_points['Date'] = pd.to_datetime(df_points['Date']).dt.date
# export data to excel
df_points.to_excel('data/data_all.xlsx', index=False)