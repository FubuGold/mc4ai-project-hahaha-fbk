import streamlit as st
import pandas as pd
from DataAnalyze import haha
from DataAnalyze import huhu
from PersonalInfo.PersonalInfoShowcase import Login_Personal_Tab

@st.cache_data
def ReadData():
    return pd.read_csv('py4ai-score.csv')

@st.cache_data
def SubDataPass(Data):
    return pd.DataFrame({
                'Username' : Data['NAME'] + Data.index.astype(str),
                'Password' : ['123456789' for _ in Data.index]
            })

def main(): 
    Data = pd.read_csv('py4ai-score.csv')
    Data.drop(['NAME','CLASS'],axis='columns',inplace=True)
    st.set_page_config(layout="wide")
    st.title('Phân tích và xem điểm Python4AI 092022')
    Data = ReadData()
    PersonalInfoTab, AnalyzeTab, DataTab = st.tabs(['Xem điểm','Phân tích thống kê','Bảng điểm tổng quát'])

    with PersonalInfoTab:
        Login_Personal_Tab(Data)
        
    with AnalyzeTab:
        st.header('Phân tích dữ liệu')
        tab1, tab2 = st.tabs(["analyze","classify"])
        with tab1:
            haha.analyze(Data)
        with tab2:
            number = int(st.slider('Number input',min_value=1,max_value=10, step = 1))
            if st.button('OK'):
                huhu.classify(Data, number)

    with DataTab:
        col1,col2 = st.columns(2)
        with col1:
            st.header('Danh sách điểm')
            st.write('Đã xáo trộn ngẫu nhiên')
            SubData_Point = Data.drop(['NAME','GENDER','CLASS'],axis='columns').sample(frac=1, random_state=69).reset_index(drop=True)
            SubData_Point["REG-MC4AI"].fillna("N", inplace = True)
            for i in range(1,11):
                 SubData_Point[f"S{i}"].fillna(0,inplace = True)
            SubData_Point["BONUS"].fillna(0,inplace = True)
            
            st.dataframe(data=SubData_Point, height=1000)

        with col2:
            st.header('Danh sách username/password mặc định')
            search = st.text_input(label='Tìm kiếm tên',placeholder='VD:nguyenvana')
            search_button = st.button('Tìm kiếm')
            SubData = SubDataPass(Data)
            if search_button:
                if search == '':
                    st.dataframe(data=SubData, height=1000)
                else:
                    st.dataframe(data=SubData.loc[SubData['Username'].str.contains(search)])

if __name__ == '__main__':
    main()