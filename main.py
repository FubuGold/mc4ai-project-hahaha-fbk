import streamlit as st
import pandas as pd
from haha import *
from huhu import *
def main(): 
    Data = pd.read_csv('py4ai-score.csv')
    Data.drop(['NAME','CLASS'],axis='columns',inplace=True)
    st.set_page_config(layout="wide")
    st.title('Phân tích và xem điểm Python4AI 092022')
    PersonalInfoTab, AnalyzeTab, DataTab = st.tabs(['Xem điểm','Phân tích thống kê','Bảng điểm tổng quát'])
    with PersonalInfoTab:
        st.header('Login')
    with AnalyzeTab:
        st.header('Phân tích dữ liệu')
        analyze(Data)
        classify(Data, 4)
    with DataTab:
        for i in range(1,11):
            Data[f"S{i}"].fillna(0, inplace = True)
        Data["BONUS"].fillna(0, inplace = True)
        Data["REG-MC4AI"].fillna("N", inplace = True)
        st.dataframe(data=Data, height=1000)

if __name__ == '__main__':
    main()