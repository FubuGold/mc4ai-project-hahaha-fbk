from sklearn.cluster import KMeans
import numpy as np
def classify(data, n):
    filter = ["S6", "S10", "GPA"]
    used_data = data[filter].fillna(0)
    kmeans = KMeans(n_clusters=n, n_init='auto')
    kmeans.fit(used_data)
    # print(kmeans.labels_)