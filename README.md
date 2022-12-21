# fitness_mockup

Libraries install: <br>
conda install pip<br>
pip install pandas<br>
pip install datetime<br>
pip install openpyxl<br>
pip install streamlit<br>
pip install plotly<br>

Versions: <br><br>
plotly == 5.9.0<br>
openpyxl == 3.0.10
<br>
Data update process:<br>
1. download new data from Strava
2. rename to data_new.csv and replace in data file
3. run python data_update.py in prompt
4. push new data to github
5. Streamlit app is updated automatically

<br>
<b>Description of files</b><br>
main.py - specifies sidebar and tabs, adds last data update information, as well as info in General Information tab.<br>
team_graph_tab.py - The Team Standings tab. It is the default home page. Shows overall stats and points by team by default. Option to switch to team points evolution graph or comparison of different people and teams with multiselect, which flows from comparison_option.py file.<br>
overview.py - Activities overview tab. By default shows list of all activities counted towards scores sorted by date. Options are to filter by date, team, or name. Filter by team shows graphs as well.<br>
milestone_tab.py - Milestone Achievement tab. Shows whether milestones were achieved - yes or no, with count of kilometers/activities.<br>
