import numpy as np
from httpx import ReadTimeout,WriteTimeout
import streamlit as st
import face_recognition as fr
from supabase import create_client
from PIL import Image

class AIFaceReg:

    known_encoding = []
    known_id = []
    

    def __init__(self) -> None:
        url = st.secrets['connect_supabase']['url']
        key = st.secrets['connect_supabase']['key']
        self.cursor = create_client(url,key)

    def FetchData(self) -> None:
        try:
            img_data = self.cursor.table('user').select('id','face_img').neq('face_img',r'[]').execute().data
            # img_data = [data for data in img_data if data['face_img'] is not None] # Filter none
            for data in img_data:
                self.known_encoding.append(data['face_img'])
                self.known_id.append(data['id'])
        except Exception as e:
            if e == ReadTimeout:
                st.warning('Kết nối với máy chủ. Xin hãy chờ')

    def UpdateImg(self,img_buffer,id) -> tuple:
        try:
            if img_buffer is None: return (False,'')
            connected = False

            # Convert image
            img_file = Image.open(img_buffer)
            img_file = np.array(img_file)

            face_loc = fr.face_locations(img_file)
            if len(face_loc) == 0:
                return (False,'Không nhận khuôn mặt')
            elif len(face_loc) > 1:
                return (False,'Có nhiều hơn 1 khuôn mặt')
            
            img_encode = fr.face_encodings(img_file)[0].tolist()
            self.cursor.table('user').update({'face_img':img_encode}).eq("id",id).execute()
            
            return (True,'Thành công')
        except Exception as e:
            if e == WriteTimeout: return(True,'Kết nối với máy chủ. Thông tin đã được nhận')
            return (False,'Đã xảy ra lỗi, vui lòng thử lại')

    def CompareInput(self,img_buffer) -> int:
        if img_buffer is None: return -1

        img_file = Image.open(img_buffer)
        img_file = np.array(img_file)

        face_loc = fr.face_locations(img_file)
        if len(face_loc) == 0:
            return -1
        elif len(face_loc) > 1:
            return -2
        
        unknown_encoding = fr.face_encodings(img_file)[0]
        res = fr.face_distance(self.known_encoding,unknown_encoding).argmin()
        return self.known_id[res]


# def test():
#     model = AIFaceReg()
#     model.FetchData()
#     # for encode in model.known_encoding:
#     #     st.write(encode)
#     img_buffer_file = st.camera_input('Check input')
#     st.write(model.CompareInput(img_buffer_file))
#     # st.write(model.UpdateImg(img_buffer_file,69))
    

# if __name__ == '__main__':
#     test()
