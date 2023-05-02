import mysql.connector
import streamlit as st
# import pandas as pd

class PasswordManager:
    database = None
    cursor = None
    user = None

    def __init__(self) -> None:
        self.database = mysql.connector.connect(host = st.secrets['host'], user = st.secrets['username'], passwd = st.secrets['password'], database = st.secrets['database'],port = st.secrets['port'])
        # self.database = mysql.connector.connect(host = 'mtv.h.filess.io',user = 'ProjectAIpassword_standstick',passwd = 'dontaskaboutpassword',database = 'ProjectAIpassword_standstick',port = 3307)
        self.cursor = self.database.cursor()

    def DefaultPassReset(self,Data) -> None:
        self.cursor.execute("DELETE FROM user")
        for i in Data.index:
            username = Data['NAME'][i] + str(i)
            self.cursor.execute("INSERT INTO user VALUE (%s,%s,%s)", (username,'123456789',i))
            self.database.commit()

    def ValidateInput(self,username : str,password : str) -> bool:
        return username.find(' ') == -1 and username.find("'") == -1 and password.find(' ') == -1 and password.find("'") == -1

    def CheckInput(self,username,password) -> bool:
        if (not self.ValidateInput(username,password)): return False
        self.cursor.execute("SELECT * FROM user WHERE username LIKE %s AND pass LIKE %s",(username,password))
        temp = []
        for x in self.cursor:
            temp.append(x)
        
        if len(temp) == 1:
            self.user = username
            return True
        else: return False

    def ValidateResetUser(self,username : str) -> bool:
        if (not self.ValidateInput(username,'123456789')): return False
        self.cursor.execute("SELECT * FROM user WHERE username LIKE %s",(username,))
        temp = self.cursor.fetchall()
        if len(temp) > 0: return False
        else: return True

    def ChangePassword(self, password : str) -> bool:
        if (not self.ValidateInput('temporary',password=password)): return False
        self.cursor.execute("UPDATE user SET pass = %s WHERE username LIKE %s",(password,self.user))
        self.database.commit()
        return True

    def ChangeUsername(self,username : str) -> bool:
        if (not self.ValidateResetUser(username)): return False
        self.cursor.execute("UPDATE user SET username = %s WHERE username LIKE %s",(username,self.user))
        self.database.commit()
        return True
    
    def PasswordRecover(self,username : str):
        if (not self.ValidateInput(username,'123456789')): return False
        self.cursor.execute("SELECT pass FROM user WHERE username like %s",(username,))
        temp = self.cursor.fetchall()
        return temp[0][0]
    
    def GetID(self):
        self.cursor.execute('SELECT ID FROM user WHERE username like %s',(self.user,))
        temp = self.cursor.fetchall()
        return temp[0][0]
    

# def test():
#     Data = pd.read_csv('py4ai-score.csv')
#     pwdman = PasswordManager()


# if __name__ == '__main__':
#     test()