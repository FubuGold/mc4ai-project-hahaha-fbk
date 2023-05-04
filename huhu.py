from sklearn.cluster import KMeans
import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd
def visualize(d, k):
    a = np.concatenate(np.array(d["S6"]).astype(int),np.array(k.cluster_centers_[:,0]).astype(int))
    b = np.concatenate(np.array(d["S10"]).astype(int), np.array(k.cluster_centers_[:,1]).astype(int))
    c = np.concatenate(np.array(d["GPA"]).astype(int),np.array(k.cluster_centers_[:,2]).astype(int))

    t = pd.DataFrame({  
                        "x": a,
                        "y": b,
                        "z": c
                    })
    
    st.plotly_chart(px.scatter_3d(t,x = "x", 
                                    y = "y", 
                                    z = "z"),theme = None)
    # print(np.array(d["S6"]).astype(int),type(np.array(d["S6"]).astype(int)))
def classify(data, n):
    filter = ["S6", "S10", "GPA"]
    used_data = data[filter].fillna(0)
    kmeans = KMeans(n_clusters=n, n_init='auto')
    kmeans.fit(used_data)
    visualize(used_data,kmeans)
    # print(kmeans.cluster_centers_.shape)
    # print(kmeans.labels_)
    