import streamlit as st
import pandas as pd

def main(): 
    st.set_page_config(layout="wide")
    st.title('Phân tích và xem điểm Python4AI 092022')
    Data = pd.read_csv('py4ai-score.csv')
    PersonalInfoTab, AnalyzeTab, DataTab = st.tabs(['Xem điểm','Phân tích thống kê','Bảng điểm tổng quát'])
    with PersonalInfoTab:
        st.header('Login')
    with AnalyzeTab:
        st.header('Phân tích dữ liệu')
    with DataTab:
        col1,col2 = st.columns(2)
        with col1:
            st.header('Danh sách điểm')
            st.write('Đã xáo trộn ngẫu nhiên')
            SubData_Point = Data.drop(['NAME','GENDER','CLASS'],axis='columns').sample(frac=1, random_state=69)
            SubData_Point.reset_index(drop=True)
            st.dataframe(data=SubData_Point, height=1000)
        with col2:
            st.header('Danh sách username, password mặc định')
            pwd_df = pd.DataFrame({
                'Username': Data['NAME'] + Data['CLASS'] + '\t\t\t\t\t\t\t\t',
                'Password': ['123456789' for _ in range(len(Data))] 
            })
            st.dataframe(data=pwd_df, height=1000)




if __name__ == '__main__':
    main()