import numpy as np
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
        img_data = self.cursor.table('user').select('id','face_img').neq('face_img',r'{}').execute().data
        # img_data = [data for data in img_data if data['face_img'] is not None] # Filter none
        for data in img_data:
            img_file = np.array(data['face_img']).astype(np.uint8)
            self.known_encoding.append(fr.face_encodings(img_file)[0])
            self.known_id.append(data['id'])
        

    def UpdateImg(self,img_buffer,id) -> tuple:
        try:
            if img_buffer is None: return (False,'')

            # Convert image
            img_file = Image.open(img_buffer)
            img_file = np.array(img_file)

            face_loc = fr.face_locations(img_file)
            if len(face_loc) == 0:
                return (False,'Không nhận khuôn mặt')
            elif len(face_loc) > 1:
                return (False,'Có nhiều hơn 1 khuôn mặt')
            
            self.cursor.table('user').update({'face_img':img_file.tolist()}).eq("id",id).execute()

            return (True,'Thành công')
        except:
            return (False,'Đã xảy ra lỗi. Vui lòng thử lại')

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
