import streamlit as st
import pandas as pd
def main(): 
    st.set_page_config(layout="wide")
    st.title('Phân tích và xem điểm Python4AI 092022')
    
    PersonalInfoTab, AnalyzeTab, DataTab = st.tabs(['Xem điểm','Phân tích thống kê','Bảng điểm tổng quát'])
    with PersonalInfoTab:
        st.header('Login')
    with AnalyzeTab:
        st.header('Phân tích dữ liệu')
    with DataTab:
        Data = pd.read_csv('py4ai-score.csv')
        Data.drop(['NAME','GENDER','CLASS'],axis='columns',inplace=True)
        st.dataframe(data=Data, height=1000)


if __name__ == '__main__':
    main()