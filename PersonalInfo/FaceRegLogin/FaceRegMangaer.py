import os
import numpy as np
import streamlit as st
import face_recognition as fr
from supabase import create_client
from PIL import Image

class AIFaceReg:
    
    folder_path = f'PersonalInfo/FaceRegLogin/testimage'
    known_encoding = None
    
    def __init__(self) -> None:
        # url = st.secrets['connect-supabase']['url']
        # key = st.secrets['connect-supabase']['key']
        url = "https://ransvclhkscfkexttzdz.supabase.co"
        key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJhbnN2Y2xoa3NjZmtleHR0emR6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODMwMzU2NTQsImV4cCI6MTk5ODYxMTY1NH0.DR0ZxeTjINgYLM5ohE_PAfQuRar-pJwf72SfLfwF0zo"
        self.cursor = create_client(url,key)

    def FetchDataFromStorage(self) -> bool:
        try:
            bucket_path = 'face_reg_database/FaceImage'
            file_list = self.cursor.storage.from_('face_reg_database').list(bucket_path)
            for file in file_list:
                if file['name'].endswith('.jpeg'):
                    st.write(file['name'])
            return True
        except:
            return False


    def QueueUpdate(self,img_buffer,id) -> bool:
        try:
            if img_buffer is None: return False
            img_path = f'{self.folder_path}/{id}.jpeg'
            if os.path.isfile(img_path):
                os.remove(img_path)
            img = Image.open(img_buffer)
            img.save(img_path)
        except:
            return False
        
    def UpdateStorage(self) -> None:
        pass

    def CompareInput(self) -> None:
        pass



def test():
    model = AIFaceReg()
    model.FetchDataFromStorage()

if __name__ == '__main__':
    test()
