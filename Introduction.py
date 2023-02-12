import streamlit as st
from utils.utils import check_authentication

st.set_page_config(layout="wide",
                   page_title='Introduction',
                   initial_sidebar_state='expanded')

authentication_status, authenticator, username = check_authentication()

if authentication_status == False:
    st.error('Incorrect username or password failed. Please try again.')

if authentication_status == None:
    st.warning('Please log in to continue.')

if authentication_status:
    authenticator.logout('Log out', 'sidebar')
    st.info('# Fall 2022: Learning & Engagement Survey Analysis')
    st.markdown(
        '*For the best viewing experience, open the menu in the top right corner, click "Settings" and choose a "Light" theme.*'
    )
    st.markdown('## 1.0 – Introduction')
    st.write(
        'On the left sidebar, there are two pages you can visit. Below is an explanation of each page.'
    )
    st.markdown('### 1.1 – Overview of all classes')
    st.markdown(
        '- On this page, you will find a visual comparison of the survey responses for a particular question across any number of selected classes. You can also select a specific year and/or program to filter the classes you are comparing.'
    )
    st.markdown('### 1.2 – Overview of a single class')
    st.markdown(
        '- On this page, you will find statistics for all quantitative survey questions for a particular class. If you select a class that you teach, you will also be able to see the additional comments that students left for your class in the survey.'
    )

    st.error(
        '**Each page provides detailed explanations of what it does, who it is for, and how to use it. Please go through each page from top to bottom and read these explanations carefully.**'
    )
