import os
import io
import numpy as np
import streamlit as st
import face_recognition as fr
from supabase import create_client
from PIL import Image

class AIFaceReg:
    
    folder_path = f'PersonalInfo/FaceRegLogin/testimage'
    bucket_path = 'face_reg_database/FaceImage'
    known_encoding = []
    known_id = []
    
    def __init__(self) -> None:
        # url = st.secrets['connect-supabase']['url']
        # key = st.secrets['connect-supabase']['key']
        url = "https://ransvclhkscfkexttzdz.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhbnN2Y2xoa3NjZmtleHR0emR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODMwMzU2NTQsImV4cCI6MTk5ODYxMTY1NH0.DR0ZxeTjINgYLM5ohE_PAfQuRar-pJwf72SfLfwF0zo"
        self.cursor = create_client(url,key)

    def FetchDataFromStorage(self) -> None:
        file_list = self.cursor.storage.from_('face_reg_database').list(self.bucket_path)
        for file in file_list:
            if file['name'].endswith('.jpeg'):
                img_file = self.cursor.storage.from_('face_reg_database').download(f'{self.bucket_path}/{file["name"]}')
                img_file = Image.open(io.BytesIO(img_file))
                tmp_encoding = fr.face_encodings(img_file)[0]
                self.known_encoding.append(tmp_encoding)
                self.known_id.append(int(file['name'].replace('.jpeg','')))

    def QueueUpdate(self,img_buffer,id) -> tuple:
        try:
            if img_buffer is None: return (False,'')
            img_path = f'{self.folder_path}/{id}.jpeg'
            img = Image.open(img_buffer)
            face_loc = fr.face_locations(img)
            if len(face_loc) == 0:
                return (False,'Không nhận khuôn mặt')
            elif len(face_loc) > 1:
                return (False,'Có nhiều hơn 1 khuôn mặt')
            if os.path.isfile(img_path):
                os.remove(img_path)
            img.save(img_path)
            return (True,'Thành công')
        except:
            return (False,'Đã xảy ra lỗi. Vui lòng thử lại')
        
    def UpdateStorage(self) -> None:
        img_name_list = os.listdir(self.folder_path)
        for img_name in img_name_list:
            img_path = f'{self.folder_path}/{img_name}'
            self.cursor.storage.from_('face_reg_database').upload(self.bucket_path,img_path)

    def CompareInput(self,img_buffer) -> int:
        img = Image.open(img_buffer)
        face_loc = fr.face_locations(img)
        if len(face_loc) == 0:
            return -1
        elif len(face_loc) > 1:
            return -2
        unknown_encoding = fr.face_encodings(img)[0]




def test():
    model = AIFaceReg()
    model.FetchDataFromStorage()

if __name__ == '__main__':
    test()
