import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
def phan_bo_diem(data, s):
    st.plotly_chart(px.histogram(data, x = s, color = "GENDER"))
def analyze(data):
    for i in range(10):
        phan_bo_diem(data, 'S' + str(i+1))
    st.plotly_chart(px.pie(data, names ='GENDER'))
    st.plotly_chart(px.pie(data, names ='PYTHON-CLASS'))
    ##########################################################
    data.replace(float('nan'), 0)  # refine the data

    average = pd.DataFrame(columns=["Session", "Average Score"])
    for i in range(1, 11): #calculate the average score of each session and add to the average dataframe
        average = average.append(
            pd.Series([f"S{i}", round(data[f"S{i}"].mean(), 1)], index=average.columns), 
            ignore_index=True
        )
    st.plotly_chart(px.bar(average, y = "Average Score", x = "Session"))