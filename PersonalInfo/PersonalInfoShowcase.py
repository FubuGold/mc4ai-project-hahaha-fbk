import streamlit as st
import pandas as pd
import plotly.express as px
from PersonalInfo.PersonalInfoManager import ComparePredictReal
from PersonalInfo.PasswordLogin.PasswordManager import PasswordManager
from PersonalInfo.FaceRegLogin.FaceRegMangaer import AIFaceReg

def PersonalInfoShowcase(Data : pd.DataFrame,ID : int):
    model = ComparePredictReal(Data)
    Data.fillna(0)
    st.markdown('## Thông tin cá nhân')
    st.table(Data[ ['NAME','GENDER','CLASS','PYTHON-CLASS','GPA','REG-MC4AI'] ].iloc[ID])

    st.markdown('## Điểm thành phần')
    homeword_label = [f'S{i}' for i in range(1,11)]
    st.dataframe(Data[homeword_label + ['BONUS']].loc[Data.index == ID].fillna(0))

    st.markdown('## Biểu đồ điểm')
    point_data = {
        'Homework':homeword_label,
        'Point': Data[homeword_label].iloc[ID].fillna(0).values
    }
    st.plotly_chart(px.line(data_frame=point_data,x='Homework',y='Point',range_y=(0,10)))

    st.markdown('## Dự đoán bằng AI Regression')
    st.table(model.CompareTable(Data.iloc[ID]))
    st.markdown("### **Nhận xét:**")
    st.markdown('Giữa **trung bình điểm homework**, **midterm exam** và **final exam** không có tính liên kết chặt chẽ, thể hiện qua độ chính xác của AI')

def Login_Personal_Tab(Data: pd.DataFrame):
    if 'login' not in st.session_state:
        st.session_state['login'] = None
    if 'face-activate' not in st.session_state:
        st.session_state['face-activate'] = False
    
    pass_mng = PasswordManager()
    face_mng = AIFaceReg()
    login_container = st.empty()
    showcase_container = st.empty()

    if st.session_state['login'] == None:
        with login_container.container():
            password_tab, face_tab = st.tabs(['Đăng nhập bằng password','Đăng nhập bằng khuôn mặt'])

            with password_tab:
                usr = st.text_input('Username',max_chars=255)
                pwd = st.text_input('Password',max_chars=255, type = 'password')
                login = st.button('Login')
                if login:
                    if usr == ' ' or pwd == ' ' or (not pass_mng.CheckInput(usr,pwd)):
                        st.error('Incorrect username/password')
                    else:
                        st.session_state['login'] = pass_mng.user_ID
                        st.experimental_rerun()
            
            with face_tab:
                st.session_state['face-activate'] = st.checkbox('Đăng nhập bằng khuôn mặt')
                if st.session_state['face-activate']:
                    face_mng.FetchData()
                    img_buffer = st.camera_input('Chụp ảnh khuôn mặt',help='Trong khung hình chỉ có 1 khuôn mặt')
                    res = face_mng.CompareInput(img_buffer)
                    if res == -1 and img_buffer is not None:
                        st.error("Không nhận thấy khuôn mặt")
                    elif res == -2:
                        st.error("Hơm 1 khuôn mặt trong ảnh")
                    elif res != -1:
                        st.write(f'Số thứ tự của bạn có phải là {res} không ? (Kiểm tra tại Danh sách điểm)')
                        st.write(f'Nếu không xin hãy thử lại')
                        if st.button('Xác nhận'):
                            st.session_state['login'] = res
                            st.experimental_rerun()

    if st.session_state['login'] != None:
        login_container.empty()
        pass_mng.user_ID = st.session_state['login']
        st.session_state['face-activation'] = False
        with showcase_container.container():
            showcase,setting = st.tabs(['Xem điểm','Cài đặt'])

            with showcase:
                PersonalInfoShowcase(Data,st.session_state['login'])
            
            with setting:
                logout = st.button('Logout')
                if logout:
                    st.session_state['login'] = None
                    st.experimental_rerun()
                
                st.write('Đổi username/password')
                change_usr = st.text_input('Change username',max_chars=255)
                change_pwd = st.text_input('Change password',max_chars=255, type='password')
                commit = st.button('Commit')
                if commit:
                    usr_state,pwd_state = None,None
                    if change_usr != '': usr_state = pass_mng.ChangeUsername(change_usr)
                    if change_pwd != '': pwd_state = pass_mng.ChangePassword(change_pwd)

                    if usr_state == True: st.success('Successfully changed username')
                    elif usr_state == False: st.error('Change username failed')
                    if pwd_state: st.success('Successfully changed password')
                    elif pwd_state == False: st.error('Change password failed')

                st.write('Cập nhập đăng nhập bằng khuôn mặt')
                st.session_state['face-activate'] = st.checkbox('Đăng ký bằng khuôn mặt')
                if st.session_state['face-activate']:
                    img_buffer = st.camera_input('Chụp hình khuôn mặt')
                    if st.button('Xác nhận'):
                        res = face_mng.UpdateImg(img_buffer,st.session_state['login'])
                        if res[0] == True:
                            st.success('Đăng kí thành công')
                        elif res[1] != '':
                            st.error(res[1])


# def test():
#     data = pd.read_csv('py4ai-score.csv')
#     PersonalInfoShowcase(data,69)
#     # Login_Personal_Tab(data)

# if __name__ == '__main__':
#     test()
        