from sklearn.cluster import KMeans
import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd
def visualize(d, k, n):
    a = np.array(d["S6"]).tolist()
    b = np.array(d["S10"]).tolist()
    c = np.array(d["GPA"]).tolist()
    label = k.labels_.tolist()
    for i in range(n): 
        label.append(n)
        a.append(k.cluster_centers_[i][0])
        b.append(k.cluster_centers_[i][1])
        c.append(k.cluster_centers_[i][2])
    t = pd.DataFrame({  
                        "x": a,
                        "y": b,
                        "z": c
                    })

    st.plotly_chart(px.scatter_3d(t,x = "x", 
                                    y = "y", 
                                    z = "z", color = label),theme = None)
    # print(np.array(d["S6"]).astype(int),type(np.array(d["S6"]).astype(int)))
def cout_datatable(d, label):
    ...
    
def classify(data, n):
    filter = ["S6", "S10", "GPA"]
    used_data = data[filter].fillna(0)
    kmeans = KMeans(n_clusters=n, n_init='auto')
    kmeans.fit(used_data)
    visualize(used_data,kmeans,n)
    ### xuất n bảng dữ liệu
    cout_datatable(used_data,kmeans.labels_)
    # print(kmeans.cluster_centers_)
    # print(kmeans.labels_)
    