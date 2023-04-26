import plotly.express as px
import matplotlib.pyplot as plt
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
    for i in range(10):
        temp = [float(j) for j in data['S'+ str(i+1)]]
        data['S'+ str(i+1)] = temp
    temp = [np.array(data['S'+ str(i+1)]).mean() for i in range(10)]
    index = [i for i in range(1,11)]
    d1 = pd.DataFrame({'avg_score' : temp,
                       'index'     : index})
    n_bins = 20
    plt.hist(d1['avg_score'], n_bins, density = True, 
         histtype ='bar')
    plt.bar(x = d1['index'], y = d1['avg_score'])
    plt.show()