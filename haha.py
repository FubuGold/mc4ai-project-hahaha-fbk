import plotly.express as px
def phan_bo_diem(data, s):
    px.histogram(data, x = s)
def analyze(data):
    for i in range(10):
        phan_bo_diem(data, "S" + str(i+1))
