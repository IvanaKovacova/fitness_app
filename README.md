# fitness_app

Libraries install: <br><br>
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
1. open git bash. cd documents, cd fitness_app
2. git pull
3. download new data from Strava
4. rename to data_new.csv and replace in data file
5. open anaconda prompt, cd documents, cd fitness_app
6. in anaconda prompt type: python data_update.py 
7. in git bash: git add .
8. git commit -m 'name of change'
9. git push
10. Streamlit app is updated automatically

<br>
<b>Description of files</b><br>
main.py - specifies sidebar and tabs, adds last data update information, as well as info in General Information tab.<br>
team_graph_tab.py - The Team Standings tab. It is the default home page. Shows overall stats and points by team by default. Option to switch to team points evolution graph or comparison of different people and teams with multiselect, which flows from comparison_option.py file.<br>
overview.py - Activities overview tab. By default shows list of all activities counted towards scores sorted by date. Options are to filter by date, team, or name. Filter by team shows graphs as well.<br>
milestone_tab.py - Milestone Achievement tab. Shows whether milestones were achieved - yes or no, with count of kilometers/activities.<br>
