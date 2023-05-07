import os
import io
import cv2
import numpy as np
import streamlit as st
import face_recognition as fr
from supabase import create_client

class AIFaceReg:
    
    folder_path = f'PersonalInfo/FaceRegLogin/cacheimage'
    bucket_path = 'face_reg_database/FaceImage'
    known_encoding = []
    known_id = []
    
    def __init__(self) -> None:
        url = st.secrets['connect-supabase']['url']
        key = st.secrets['connect-supabase']['key']
        # url = "https://ransvclhkscfkexttzdz.supabase.co"
        # key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhbnN2Y2xoa3NjZmtleHR0emR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODMwMzU2NTQsImV4cCI6MTk5ODYxMTY1NH0.DR0ZxeTjINgYLM5ohE_PAfQuRar-pJwf72SfLfwF0zo"
        self.cursor = create_client(url,key)

    def FetchData(self) -> None:
        file_list = self.cursor.storage.from_('face_reg_database').list(self.bucket_path)
        st.write(file_list)
        for file in file_list:
            if file['name'].endswith('.jpg'):
                img_file_byte = self.cursor.storage.from_('face_reg_database').download(f'{self.bucket_path}/{file["name"]}')
                img_file = cv2.imdecode(np.frombuffer(img_file_byte, np.uint8), cv2.IMREAD_COLOR)

                tmp_encoding = fr.face_encodings(img_file)[0]
                self.known_encoding.append(tmp_encoding)
                self.known_id.append(int(file['name'].replace('.jpg','')))

    def QueueUpdate(self,img_buffer,id) -> tuple:
        try:
            if img_buffer is None: return (False,'')

            img_path = f'{self.folder_path}/{id}.jpg'
            img_file_byte = img_buffer.getvalue()
            img_file = cv2.imdecode(np.frombuffer(img_file_byte, np.uint8), cv2.IMREAD_COLOR)

            face_loc = fr.face_locations(img_file)
            if len(face_loc) == 0:
                return (False,'Không nhận khuôn mặt')
            elif len(face_loc) > 1:
                return (False,'Có nhiều hơn 1 khuôn mặt')
            
            if os.path.isfile(img_path):
                os.remove(img_path)
            cv2.imwrite(img_path,img_file)
            return (True,'Thành công')
        except:
            return (False,'Đã xảy ra lỗi. Vui lòng thử lại')
        
    def UpdateStorage(self) -> None:
        img_name_list = os.listdir(self.folder_path)
        _bucket_file_list = self.cursor.storage.from_('face_reg_database').list(self.bucket_path)
        _bucket_file_list = [file['name'] for file in _bucket_file_list]
        for img_name in img_name_list:
            img_path = f'{self.folder_path}/{img_name}'
            img_save_path = f'{self.bucket_path}/{img_name}'

            if img_name in _bucket_file_list: # Remove if exist
                self.cursor.storage.from_('face_reg_database').remove(img_save_path)
            
            self.cursor.storage.from_('face_reg_database').upload(img_save_path,img_path,
                                                                {"content-type": "image/jpg"})


    def ClearCache(self) -> None:
        img_name_list = os.listdir(self.folder_path)
        for img_name in img_name_list:
            img_path = f'{self.folder_path}/{img_name}'
            os.remove(img_path)

    def CompareInput(self,img_buffer) -> int:
        if img_buffer is None: return -1
        img_file_byte = img_buffer.getvalue()
        img_file = cv2.imdecode(np.frombuffer(img_file_byte, np.uint8), cv2.IMREAD_COLOR)
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
#     model.UpdateStorage()
#     model.FetchDataFromStorage()
#     st.write(model.known_id)
#     img_buffer_file = st.camera_input('Check input')
#     res = model.CompareInput(img_buffer=img_buffer_file)
#     st.write(res)
#     st.write(model.known_id)
#     st.write(model.known_encoding)
#     if st.button('Clear Cache'):
#         model.ClearCache()
    

# if __name__ == '__main__':
#     test()
