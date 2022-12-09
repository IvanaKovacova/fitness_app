import streamlit as st

def general():
    st.header('General Information')
    st.subheader('Links')
    url='https://www.strava.com/clubs/DCFC'
    st.write("[Strava Club](%s)" % url)
    
    
    st.subheader('Downloads')

    with open("data/rulebook.pdf", "rb") as pdf_file:
        pdf = pdf_file.read()
        
    st.download_button(label="Download Rulebook",
                       data=pdf,
                       file_name="Rulebook.pdf",
                       mime='application/octet-stream')
        
    with open("data/Fitness Challenge.pdf", "rb") as pdf_file:
        pdf = pdf_file.read()

    st.download_button(label="Download Points Calculation Overview",
                       data=pdf,
                       file_name="Fitness Challenge.pdf",
                       mime='application/octet-stream')
    
    st.subheader('Contacts')
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('***If you have any questions contact:***')
        st.write('Subramita Dash - subramita_dash@dell.com')
        st.write('Madhav Parashar - madhav_parashar@dell.com')
        st.write('Sanjay Kumar - sanjay_kumar29@dell.com')
        st.write('Ivana Kovacova - ivana.kovacova@dell.com')
    with col2:
        st.markdown('***For issues with the app:***')
        st.write('Ivana Kovacova - ivana.kovacova@dell.com')

def faq():
    st.header('Frequently Asked Questions')
    st.subheader('How do I track my activities?')
    st.write('There are two options:')
    st.write('1st option: Record through the app on your phone')
    st.image('img/log_activity.png')
    st.write('2nd option: Pair the app with supported smartwatch/device - list [HERE](https://support.strava.com/hc/en-us/articles/223297187-How-to-get-your-Activities-to-Strava#devices)')
    st.write('After syncing, the activities recorded on the device will appear in your Strava account')  
    st.subheader('How do I record activities that are not in the options on Strava?')
    st.write("Choose either the closest activity offered or 'workout' and then edit the name to the activity you did.")
    st.subheader('How do I record the distance of swimming activities?')
    st.write('If you do not have a waterproof smartwatch, the best option is to count your laps, multiply by the pool length and add as a manual activity.')
    st.write('If you start recording on your phone, it will only track time and you will not be able to edit distance afterwards.')
    st.subheader('My activity was not recorded right. What do I do?')
    st.write('Contact the organizers. Names and e-mails can be found in the General Information tab.')
    st.subheader('Strava is offering me paid account. Do I need it?')
    st.write('No. You can record activities in the free account as well. The paid account offers mostly analysis of your activities.')