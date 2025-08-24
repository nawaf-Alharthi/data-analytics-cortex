import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Hospital Bed Monitoring Dashboard")

# Load your data
df = pd.read_csv("ER MOH Beds.csv")
# Calculate %
df['Monitored Bed %'] = (df['Beds with Monitors'] / df['Total']) * 100
df['Monitored Bed %'] = df['Monitored Bed %'].round(2)

# Readiness classification
def classify_readiness(percent):
    if percent >= 70:
        return 'High'
    elif percent >= 50:
        return 'Medium'
    else:
        return 'Low'

df['Readiness Level'] = df['Monitored Bed %'].apply(classify_readiness)

# Priority Score
df['Priority Score'] = df['Total'] * (1 - df['Monitored Bed %'] / 100)

# Bar chart
fig = px.bar(df.sort_values('Monitored Bed %', ascending=False),
             x='Health Region', y='Monitored Bed %',
             color='Readiness Level',
             title='Monitored Bed % by Health Region',
             text='Monitored Bed %')

st.plotly_chart(fig)

# Show table
st.subheader("Data Table")
st.dataframe(df[['Health Region', 'Monitored Bed %', 'Readiness Level', 'Priority Score']])
