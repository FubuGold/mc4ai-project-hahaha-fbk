import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st
def phan_bo_diem(data, s):
    st.plotly_chart(px.histogram(data, x = s,range_x=(0,10), color = "GENDER"), theme = None)
def analyze(data):
    col1, col2 = st.columns(2)
    with col1:
        for i in range(1,10,2):
            phan_bo_diem(data, 'S' + str(i))
    with col2:
        for i in range(2,11, 2):
            phan_bo_diem(data, 'S' + str(i))
    st.write('''

    Kết luận:\n
        - Phân bố điểm giữa các session không đồng đều.\n
        - Đa số đạt điểm tối đa.\n
        - Điểm số của S10 được rải đều, và là Session có nhiều dưới trung bình nhất.\n
        --> Session 10 (Final exam) có độ khó cao nhất.\n
        --> Các Session khác điểm cao có thể không nhờ vào năng lực thực.\n

    ''')
    col1, col2 = st.columns(2)
    col1.header("Phân bố Nam Nữ")
    col1.plotly_chart(px.pie(data, names ='GENDER'),theme = None)
    col1.write("Nam Nữ khá đồng đều nhưng Nam vẫn chiếm đa số")
    col2.header("Phân bố học sinh các lớp")
    col2.plotly_chart(px.pie(data, names ='PYTHON-CLASS'), theme = None)
    col2.write("Học sinh được các thầy chia vô các lớp với số lượng đồng đều")
    ##########################################################
    st.header("Điểm trung bình từng session")
    data.replace(float('nan'), 0)
    average = pd.DataFrame(columns=["Session", "Average Score"])
    for i in range(1, 11): 
        average.loc[len(average.index)] = [f"S{i}", round(data[f"S{i}"].mean(), 1)]
    
    st.plotly_chart(px.bar(average, y = "Average Score", x = "Session"), theme = None)
    st.write('''

    Kết luận:\n
        - Session có điểm trung bình cao nhất là: Session 1.\n
        - Session có điểm trung bình thấp nhất là: Session 10 (Final).\n
        --> Khẳng định lại: "Session 10 (Final) có độ khó cao nhất."\n
        - Theo tương quan, điểm trung bình các Session cao đều trên 8(trừ Midterm 7.5 và Final 6.1).\n
        
    ''')

# def test():
#     Data = pd.read_csv('py4ai-score.csv')
#     analyze(Data)

# if __name__ == '__main__':
#     test()