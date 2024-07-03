import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Sidebar Code

st.sidebar.title("Upload dataset")
upload_file = st.sidebar.file_uploader('Choose Csv File',type='csv')
if upload_file is not None:
    data = pd.read_csv(upload_file)
    no_event = len(data)
    citizenship_counts = data['citizenship'].value_counts()
    event_location_region = data['event_location_region'].value_counts()
    hostilities_counts = data[data['took_part_in_the_hostilities'] == 'Yes']['citizenship'].value_counts()
    no_hostilities_counts = data[data['took_part_in_the_hostilities'] == 'No']['citizenship'].value_counts()

    st.sidebar.write('No of Event :',no_event)

    col1,col2 = st.sidebar.columns(2)
    col3,col4 = st.sidebar.columns(2)
    with col1:
        st.subheader('Citizenship_counts')
        st.write(citizenship_counts)
    with col2:
        st.subheader('Event_location_region')
        st.write(event_location_region)
    with col1:
        st.subheader('Hostilities_counts')
        st.write(hostilities_counts)
    with col1:
        st.subheader('No_hostilities_counts')
        st.write(no_hostilities_counts)
    
    weapons_counts = data['ammunition'].value_counts()
    st.sidebar.write('Weapons_counts',weapons_counts)

# Data Analysis

st.title("Isreal Palestine Conflict Analysis")
st.write('Dataset Sample',data)

col1,col2 = st.columns(2)
with col1:
    st.subheader('Types of injuries')
    type_of_injury = data['type_of_injury'].value_counts()
    st.bar_chart(type_of_injury)
with col2:
    st.subheader('Male Female Count')
    MF_count = data['gender'].value_counts()
    st.bar_chart(MF_count,color='#ffaa00')

col1,col2 = st.columns(2)
with col1:
    st.subheader('Age Summary')
    age = data['age'].describe()
    st.write(age)
with col2:
    st.subheader('Event Location Region Count')
    event_location_region = data['event_location_region'].value_counts()
    st.bar_chart(event_location_region,color='#0000ff')


col1,col2 = st.columns(2)
with col1:
    redence_count = data.groupby('event_location_region')['place_of_residence'].nunique()
    st.subheader('Residence Percentage by Region')
    fig,ax = plt.subplots()
    ax.pie(redence_count,labels =redence_count.index ,autopct = '%1.1f%%')
    st.pyplot(fig)

# Average Region
with col2:
    region_average = data.groupby('event_location_region')['age'].mean()
    st.subheader("Avg Age by Region")
    st.bar_chart(region_average,color='#ffaa0088')

col1,col2 = st.columns(2)
with col1:
    nationality_count = data.groupby('citizenship').size().reset_index(name='incident_count')
    st.subheader('Incident Count by Nationality')
    st.write(nationality_count)
with col2:
    genderInc = data.groupby('gender').size().reset_index(name='incident_count')
    st.subheader('Incident Count by Gender')
    st.write(genderInc)

# Time Based Analysis

data['date_of_event'] = pd.to_datetime(data['date_of_event'])
data['year'] = data['date_of_event'].dt.year
data['month'] = data['date_of_event'].dt.month_name()  # Format month as month name
time_events = data.groupby(['year', 'month']).size().reset_index(name='incident_count')
time_events['year_month'] = time_events['month'] + ' ' + time_events['year'].astype(str)
st.subheader('Time-Based Events')
st.line_chart(time_events.set_index('year_month')['incident_count'])