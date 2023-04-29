import streamlit as st
import pandas as pd
from PersonalInfoManager import ComparePredictReal

@st.cache_data
def ReadData():
    return pd.read_csv('py4ai-score.csv')

def PersonalInfoShowcase(Data, UserID):
    model = ComparePredictReal(Data, Data.iloc[UserID])
    st.markdown('## Điểm cá nhân')
    st.table(Data.iloc[UserID])
    st.markdown('## Dự đoán bằng AI Regression')
    st.table(model.CompareTable())
    st.markdown("### **Nhận xét:**")
    st.markdown('Giữa **trung bình điểm homework**, **midterm exam** và **final exam** không có tính liên kết chặt chẽ, thể hiện qua độ chính xác của AI')

def main(): 
    st.set_page_config(layout="wide")
    st.title('Phân tích và xem điểm Python4AI 092022')
    Data = ReadData()
    PersonalInfoTab, AnalyzeTab, DataTab = st.tabs(['Xem điểm','Phân tích thống kê','Bảng điểm tổng quát'])

    with PersonalInfoTab:
        placeholder = st.empty()
        with placeholder.container():
            PersonalInfoShowcase(Data,105)
        
    with AnalyzeTab:
        st.header('Phân tích dữ liệu')

    with DataTab:
        st.header('Danh sách điểm')
        st.write('Đã xáo trộn ngẫu nhiên')
        SubData_Point = Data.drop(['NAME','GENDER','CLASS'],axis='columns').sample(frac=1, random_state=69)
        SubData_Point.reset_index(drop=True)
        st.dataframe(data=SubData_Point, height=1000)





if __name__ == '__main__':
    main()