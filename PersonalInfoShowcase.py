import streamlit as st
import pandas as pd
from PersonalInfoManager import ComparePredictReal
from PasswordManager import PasswordManager

def PersonalInfoShowcase(Data,ID):
    model = ComparePredictReal(Data)
    st.header('Xem điểm')
    st.markdown('## Điểm cá nhân')
    st.table(Data.iloc[ID])
    st.markdown('## Dự đoán bằng AI Regression')
    st.table(model.CompareTable(Data.iloc[ID]))
    st.markdown("### **Nhận xét:**")
    st.markdown('Giữa **trung bình điểm homework**, **midterm exam** và **final exam** không có tính liên kết chặt chẽ, thể hiện qua độ chính xác của AI')

def Login_Personal_Tab(Data):
    if 'login' not in st.session_state:
        st.session_state['login'] = None
    pass_mng = PasswordManager()
    login_container = st.empty()
    showcase_container = st.empty()
    if st.session_state['login'] == None:
        with login_container.container():
            usr = st.text_input('Username',placeholder = 'Please enter your username',max_chars=255)
            pwd = st.text_input('Password',placeholder = 'Please enter your password',max_chars=255)
            login = st.button('Login')
            if login:
                if usr == ' ' or pwd == ' ' or (not pass_mng.CheckInput(usr,pwd)):
                    st.error('Username/Password incorrect')
                else:
                    st.session_state['login'] = pass_mng.GetID()

    if st.session_state['login'] != None:
        login_container.empty()
        with showcase_container.container():
            logout = st.button('Logout')
            if logout:
                st.session_state['login'] = None
                st.experimental_rerun()
            PersonalInfoShowcase(Data,st.session_state['login'])


# def test():
#     data = pd.read_csv('py4ai-score.csv')
#     Login_Personal_Tab(data)

# if __name__ == '__main__':
#     test()
        