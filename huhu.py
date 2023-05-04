from sklearn.cluster import KMeans
import numpy as np
import streamlit as st
import plotly.express as px
def visualize(d, k):
    st.plotly_chart(px.scatter_3d(d, x = "S6", y = "S10", z = "GPA", color = k.labels_))
def classify(data, n):
    filter = ["S6", "S10", "GPA"]
    used_data = data[filter].fillna(0)
    kmeans = KMeans(n_clusters=n, n_init='auto')
    kmeans.fit(used_data)
    visualize(used_data,kmeans)
    # print(kmeans.labels_)