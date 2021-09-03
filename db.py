from werkzeug.security import generate_password_hash,check_password_hash
from web import mysql



class Users:
    def __init__(self,Id,name,email,psw,apikey):
        self.Id=Id 
        self.Username=name
        self.Email=email
        self.Password=psw 
        self.apikey=apikey
        self.cur=mysql.connection.cursor()

    def check_signup(self):
        self.cur.execute("SELECT * FROM users WHERE Email='{}'".format(self.Email))
        account=self.cur.fetchone()
        if account:
            return False
        else:
            self.cur.execute("INSERT INTO users(ID,USERNAME,EMAIL,PSW,API) VALUES('{0}','{1}','{2}','{3}','{4}')".format(self.Id,self.Username,self.Email,generate_password_hash(self.Password),self.apikey))
            mysql.connection.commit()
            self.cur.close()  
    def check_login(self):
        self.cur.execute("SELECT * FROM users WHERE Email='{}'".format(self.Email))
        account=self.cur.fetchone()
        if not account:
            return False 
        else:
            if check_password_hash(account[3],self.Password)==True:
                return True 
            else:
                pass
    def get_id(self): 
        self.cur.execute("SELECT ID,API FROM users WHERE Email='{}'".format(self.Email))
        user=self.cur.fetchone()
        return user

    def check_api(self):
        self.cur.execute("SELECT * FROM users WHERE ID='{0}' AND API='{1}'".format(self.Id,self.apikey))
        check=self.cur.fetchone()
        if check:
            return True 
        else:
            return False
    def get_user(self):
        self.cur.execute("SELECT USERNAME,EMAIL FROM users WHERE ID='{0}' AND API='{1}'".format(self.Id,self.apikey))
        user=self.cur.fetchone()
        return user

    def update_api(self):
        self.cur.execute("UPDATE users SET API='{0}' WHERE ID='{1}'".format(self.apikey,self.Id))
        mysql.connection.commit()
        self.cur.close()
    
    def check_psw(self):
        self.cur.execute("SELECT PSW FROM users WHERE ID='{}'".format(self.Id))
        psw=self.cur.fetchone()
        if check_password_hash(psw[0],self.Password)==True:
            return True
        else:
            return False
    def update_psw(self):
        self.cur.execute("UPDATE users SET PSW='{0}' WHERE ID='{1}'".format(generate_password_hash(self.Password),self.Id))
        mysql.connection.commit()
        self.cur.close()
    





class Channel():
    def __init__(self,dt,temp,humi,soil,flow,idchannel):
        self.DT=dt 
        self.Temp=temp
        self.Humi=humi
        self.Soil=soil
        self.Flow=flow
        self.Idchannel=idchannel
        self.cur=mysql.connection.cursor()

    def update_value(self):
        self.cur.execute("INSERT INTO CHANNEL(DT,TEMP,HUMI,SOIL,FLOW,IDCHANNEL) VALUES('{0}','{1}',{2},'{3}','{4}','{5}')".format(self.DT,self.Temp,self.Humi,self.Soil,self.Flow,self.Idchannel))
        mysql.connection.commit()
        self.cur.close()  
    def get_value(self):
        self.cur.execute("SELECT DT,TEMP,HUMI,SOIL,FLOW FROM CHANNEL WHERE id=(SELECT max(id) FROM CHANNEL WHERE IDCHANNEL='{}')".format(self.Idchannel))
        info=self.cur.fetchone()
        return info



class Led():
    def __init__(self,light,idcontrol):
        self.Light=light
        self.Idcontrol=idcontrol
        self.cur=mysql.connection.cursor()

    def update_state(self):
        self.cur.execute("INSERT INTO LED(LIGHT,IDCONTROL) VALUES('{0}','{1}')".format(self.Light,self.Idcontrol))
        mysql.connection.commit()
        self.cur.close()
    def get_state(self):
        self.cur.execute("SELECT LIGHT FROM LED WHERE id=(SELECT max(id) FROM LED WHERE IDCONTROL='{}')".format(self.Idcontrol))
        state=self.cur.fetchone()
        return state

class Humi():
    def __init__(self,humidifier,idcontrol):
        self.Humidifier=humidifier
        self.Idcontrol=idcontrol
        self.cur=mysql.connection.cursor()
    def update_state(self):
        self.cur.execute("INSERT INTO HUMI(HUMIDIFIER,IDCONTROL) VALUES('{0}','{1}')".format(self.Humidifier,self.Idcontrol))
        mysql.connection.commit()
        self.cur.close()
    def get_state(self):
        self.cur.execute("SELECT HUMIDIFIER FROM HUMI WHERE id=(SELECT max(id) FROM HUMI WHERE IDCONTROL='{}')".format(self.Idcontrol))
        state=self.cur.fetchone()
        return state

class Pump():
    def __init__(self,pump,idcontrol):
        self.Pump=pump
        self.Idcontrol=idcontrol
        self.cur=mysql.connection.cursor()
    def update_state(self):
        self.cur.execute("INSERT INTO PUMPS(PUMP,IDCONTROL) VALUES('{0}','{1}')".format(self.Pump,self.Idcontrol))
        mysql.connection.commit()
        self.cur.close()
    def get_state(self):
        self.cur.execute("SELECT PUMP FROM PUMPS WHERE id=(SELECT max(id) FROM PUMPS WHERE IDCONTROL='{}')".format(self.Idcontrol))
        state=self.cur.fetchone()
        return state

class Water():
    def __init__(self,water,idcontrol):
        self.Water=water
        self.Idcontrol=idcontrol
        self.cur=mysql.connection.cursor()
    def update_state(self):
        self.cur.exeute("INSERT INTO WATERS(WATER,IDCONTROL) VALUES('{0}','{1}')".format(self.Water,self.Idcontrol))
        mysql.connection.commit()
        self.cur.close()
    def get_state(self):
        self.cur.execute("SELECT WATER FROM WATERS WHERE id=(SELECT max(id) FROM WATERS WHERE IDCONTROL='{}')".format(self.Idcontrol))
        state=self.cur.fetchone()
        return state














