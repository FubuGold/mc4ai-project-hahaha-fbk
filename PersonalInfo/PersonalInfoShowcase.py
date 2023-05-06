import streamlit as st
import pandas as pd
from PersonalInfo.PersonalInfoManager import ComparePredictReal
from PersonalInfo.PasswordLogin.PasswordManager import PasswordManager

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
    if 'passsowrdrecover' not in st.session_state:
        st.session_state['passwordrecover'] = None
    pass_mng = PasswordManager()
    login_container = st.empty()
    pwdrecover_container = st.empty()
    showcase_container = st.empty()

    if st.session_state['login'] == None:
        with login_container.container():
            usr = st.text_input('Username',placeholder = 'Please enter your username',max_chars=255)
            pwd = st.text_input('Password',placeholder = 'Please enter your password',max_chars=255, type = 'password')
            login = st.button('Login')
            if login:
                if usr == ' ' or pwd == ' ' or (not pass_mng.CheckInput(usr,pwd)):
                    st.error('Incorrect username/password')
                else:
                    st.session_state['login'] = pass_mng.user_ID
                    st.experimental_rerun()

    if st.session_state['login'] != None:
        login_container.empty()
        pass_mng.user_ID = st.session_state['login']
        with showcase_container.container():
            showcase,setting = st.tabs(['Xem điểm','Cài đặt'])

            with showcase:
                PersonalInfoShowcase(Data,st.session_state['login'])
            
            with setting:
                logout = st.button('Logout')
                if logout:
                    st.session_state['login'] = None
                    st.experimental_rerun()
                
                change_usr = st.text_input('Change username',max_chars=255)
                change_pwd = st.text_input('Change password',max_chars=255)
                commit = st.button('Commit')

                if commit:
                    usr_state,pwd_state = None,None
                    if change_usr != '': usr_state = pass_mng.ChangeUsername(change_usr)
                    if change_pwd != '': pwd_state = pass_mng.ChangePassword(change_pwd)

                    if usr_state == True: st.success('Successfully changed username')
                    elif usr_state == False: st.error('Change username failed')
                    if pwd_state: st.success('Successfully changed password')
                    elif pwd_state == False: st.error('Change password failed')
            


def test():
    data = pd.read_csv('py4ai-score.csv')
    Login_Personal_Tab(data)

if __name__ == '__main__':
    test()
        