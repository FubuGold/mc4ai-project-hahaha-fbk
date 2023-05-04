import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
def phan_bo_diem(data, s):
    st.plotly_chart(px.histogram(data, x = s, color = "GENDER"))
def analyze(data):
    col1, col2 = st.columns(2)
    with col1:
        for i in range(1,10,2):
            phan_bo_diem(data, 'S' + str(i))
    with col2:
        for i in range(2,11, 2):
            phan_bo_diem(data, 'S' + str(i))
    col1, col2 = st.columns(2)
    col1.header("Phân bố Nam Nữ")
    col1.plotly_chart(px.pie(data, names ='GENDER'))
    col2.header("Phân bố học sinh các lớp")
    col2.plotly_chart(px.pie(data, names ='PYTHON-CLASS'))
    ##########################################################
    st.header("Điểm trung bình từng session")
    data.replace(float('nan'), 0)
    average = pd.DataFrame(columns=["Session", "Average Score"])
    for i in range(1, 11): 
        average = average.append(
            pd.Series([f"S{i}", round(data[f"S{i}"].mean(), 1)], index=average.columns), 
            ignore_index=True
        )
    st.plotly_chart(px.bar(average, y = "Average Score", x = "Session"))