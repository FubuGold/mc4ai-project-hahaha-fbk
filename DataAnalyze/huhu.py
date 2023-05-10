from sklearn.cluster import KMeans
import numpy as np
import streamlit as st
import plotly.express as px
import pandas as pd
def visualize(d, k, n):
    a = np.array(d["S6"]).tolist()
    b = np.array(d["S10"]).tolist()
    c = np.array(d["GPA"]).tolist()
    temp = k.labels_.tolist()
    for i in range(n): 
        temp.append("Cluster")
        a.append(k.cluster_centers_[i][0])
        b.append(k.cluster_centers_[i][1])
        c.append(k.cluster_centers_[i][2])
    t = pd.DataFrame({  
                        "S6": a,
                        "S10": b,
                        "GPA": c,
                        "Group" : temp
                    })

    st.plotly_chart(px.scatter_3d(t,x = "S6", range_x=(0,10),
                                    y = "S10", range_y=(0,10),
                                    z = "GPA", range_z=(0,10),color = "Group"),theme = None)


def cout_datatable(n, d, label):
    # GPA, cao, thấp
    col1,t = st.columns(2)
    with col1:
        datatables = [d[label == i] for i in range(n)]
        for i in range(len(datatables)):
            hm = datatables[i]
            st.write(f'''Group {i}: 
            GPA cao nhất   {hm['GPA'].max()}, 
            thấp nhất    {hm['GPA'].min()}, 
            trung bình   {round(hm['GPA'].mean(),1)}''')
            st.dataframe(hm)
    
def classify(data, n):
    filter = ["S6", "S10", "GPA"]
    used_data = data[filter].fillna(0)
    kmeans = KMeans(n_clusters=n, n_init='auto')
    kmeans.fit(used_data)
    visualize(used_data,kmeans,n)
    ### xuất n bảng dữ liệu
    cout_datatable(n, used_data,kmeans.labels_)