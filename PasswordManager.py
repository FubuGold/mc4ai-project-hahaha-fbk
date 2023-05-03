from supabase import create_client
import streamlit as st
import pandas as pd
import hashlib

class PasswordManager:
    cursor = None
    user_ID = None

    def __init__(self) -> None:
        # self.database = mysql.connector.connect(host = st.secrets['host'], user = st.secrets['username'], passwd = st.secrets['password'], database = st.secrets['database'],port = st.secrets['port'])
        # self.database = mysql.connector.connect(host = 'mtv.h.filess.io',user = 'ProjectAIpassword_standstick',passwd = 'dontaskaboutpassword',database = 'ProjectAIpassword_standstick',port = 3307)
        # self.cursor = self.database.cursor()
        url = st.secrets['connect_supabase']['url']
        key = st.secrets['connect_supabase']['key']
        self.cursor = create_client(url,key)

    # def __enter__(self):
    #     email = st.secrets['user_info']['email']
    #     password = st.secrets['user_info']['password']
    #     self.cursor.auth.sign_in_with_password({"email":email, "password" : password})
        
    # def __exit__(self,*arg):
    #     self.cursor.auth.sign_out()
    

    def hashing(self,val) -> str:
        hashing = hashlib.sha512()
        hashing.update(val)
        return hashing.hexdigest()

    def DefaultPassReset(self,Data) -> None:
        # user = self.cursor.auth.get_user()
        # print(user)
        self.cursor.table("user").delete()
        hash_pwd = self.hashing('123456789'.encode())
        for i in Data.index:
            username = Data['NAME'][i] + str(i)
            self.cursor.table("user").insert({'username':username,'pass':hash_pwd,'id':i}).execute()

    def ValidateInput(self,username : str,password : str) -> bool:
        return username.find(' ') == -1 and username.find("'") == -1 and password.find(' ') == -1 and password.find("'") == -1

    def CheckInput(self,username : str,password :str) -> bool:
        if (not self.ValidateInput(username,password)): return False
        hash_pwd = self.hashing(password.encode())
        temp = self.cursor.table("user").select("*",count='exact').match({"username":username, "pass":hash_pwd}).execute()
        if temp.count == 1:
            self.user_ID = temp.data[0]['id']
            return True
        else: return False

    def ValidateResetUser(self,username : str) -> bool:
        if (not self.ValidateInput(username,'123456789')): return False
        temp = self.cursor.table("user").select("*",count='exact').eq("username",username).execute().count
        if temp > 0: return False
        else: return True

    def ChangePassword(self, password : str) -> bool:
        if (not self.ValidateInput('temporary',password)): return False
        hash_pwd = self.hashing(password.encode())
        self.cursor.table("user").update({"pass":hash_pwd}).eq("id",self.user_ID).execute()
        return True

    def ChangeUsername(self,username : str) -> bool:
        if (not self.ValidateResetUser(username)): return False
        self.cursor.table("user").update({"username":username}).eq("id",self.user_ID).execute()
        return True
    

def test():
    # Data = pd.read_csv('py4ai-score.csv')
    pwdman = PasswordManager()
    # with pwdman:
        # pwdman.DefaultPassReset(Data)
    usr = input('Username: ')
    pwd = input('Password: ')
    if pwdman.CheckInput(usr,pwd):
        print('Logined')
        pwdman.ChangePassword(input('Change password: '))



if __name__ == '__main__':
    test()