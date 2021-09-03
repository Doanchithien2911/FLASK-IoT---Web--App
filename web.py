from flask import Flask,render_template,request,redirect,url_for,session,flash,make_response,jsonify
from datetime import timedelta
from flask_mysqldb import MySQL
from db import *
import string
import json
from datetime import datetime
import math
import random 
import time

app=Flask(__name__,template_folder='template')
mysql=MySQL(app)



app.secret_key="0811"
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your database password'
app.config['MYSQL_DB'] = 'iotdb'
app.permanent_session_lifetime=timedelta(minutes=5)





@app.route('/signup',methods=["POST","GET"])
def signup():
    if request.method=="POST":
        name=request.form["Name"]
        email=request.form["Email"]
        psw=request.form["psw"]
        repeat_psw=request.form["psw-repeat"]
        if psw!=repeat_psw:
            flash("password incorrespond!")
        elif len(psw)<8:
            flash("password too weak!")
        else:
            Id=random.randint(100000,999999)
            api=string.ascii_uppercase
            apikey=''.join(random.choice(api) for i in range(20))
            user=Users(Id,name,email,psw,apikey)
            check=user.check_signup()
            if check==False:
                flash("account existing !")
            else:
                session.permanent=True
                session["id"]=Id 
                session["api"]=apikey
                return redirect(url_for("user"))
    return render_template("signup.html")




@app.route('/',methods=["POST","GET"])
def home():
    if request.method=="POST":
        email=request.form["Email"]
        psw=request.form["psw"]
        user=Users("","",email,psw,"")
        check=user.check_login()
        if check==False:
            flash("You haven't registered!")
        else:
            if check!=True:
                flash("Password is wrong!")
            else:
                session.permanent=True
                channel=user.get_id()
                idchannel=channel[0]
                apichannel=channel[1]
                session["id"]=idchannel
                session["api"]= apichannel
                return redirect(url_for("channel",ID=idchannel))
    else:
        if "id" in session:
            return redirect(url_for("channel",ID=session["id"]))
    
    return render_template("index.html")




@app.route('/channel/<int:ID>',methods=["POST","GET"])
def channel(ID):
    if "id" in session and "api" in session:
        Id=session["id"]
        if ID!=Id:
            return "Not found"
        else:
            api=session["api"]
            info=[Id,api]
            return render_template("user.html",val=info)
    else:
        flash("Please login!")
        return redirect(url_for("home"))



@app.route('/channel/user/',methods=["POST","GET"])
def user():
    if "id" in session and "api" in session:
        Id=session["id"]
        api=session["api"]
        usr=Users(Id,"","","",api)
        usr=usr.get_user()
        info=[usr[0],usr[1],Id,api]
        return render_template("acc.html",val=info)
    else:
        flash("Please login!")
        return redirect(url_for("home"))


@app.route('/channel/setting/',methods=["POST","GET"])
def setting():
    err=""
    if "id" in session and "api" in session:
        Id=session["id"]
        if request.method=="POST":
            if request.form["btn"]=="CHANGE API":
                apiChange=string.ascii_uppercase
                apiChange=''.join(random.choice(apiChange) for i in range(20))
                session["api"]=apiChange
                usrRevise=Users(Id,"","","",apiChange)
                usrRevise.update_api()
            else:
                oPsw=request.form["opsw"]
                nPsw=request.form["npsw"]
                check=Users(Id,"","",oPsw,"")
                check=check.check_psw()
                if check==True:
                    update_psw=Users(Id,"","",nPsw,"")
                    update_psw.update_psw()
                    err="Password was saved!"
                else:
                    err="Password incorrect!"    
        Api=session["api"]
        val=[Id,Api,err]
        return render_template("setting.html",value=val)
    else:
        flash("Please login!")
    return redirect(url_for("home"))


@app.route('/channel/<int:ID>/api/read/<string:apikey>',methods=["POST","GET"])
def get(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        pass 
    else:
        device=Channel("","","","","",ID)
        data=device.get_value()
        response=make_response(json.dumps(data))
        response.content_type="application/json"
        return response,200


@app.route('/channel/<int:ID>/api/write/<string:apikey>',methods=["POST","GET"])
def post(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        return "<h1>not found</h1>"
    else:
        if request.method=="POST":
            x = datetime.now()
            time=x.strftime("%X")
            data=request.get_json()
            temp=data["temp"]
            humi=data["humi"]
            soil=data["soil"]
            flow=data["flow"]
            update=Channel(time,temp,humi,soil,flow,ID)
            update.update_value()
        return '{"temp":"value","humi":"value","soil":"value","flow":"value"}'



@app.route('/channel/<int:ID>/api/get/led/<string:apikey>',methods=["POST","GET"])
def getLed(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        pass 
    else:
        device=Led("",ID)
        data=device.get_state()
        response=make_response(json.dumps(data))
        response.content_type="application/json"
        return response,200



@app.route('/channel/<int:ID>/api/post/led/<string:apikey>',methods=["POST","GET"])
def postLed(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        return "<h1>not found</h1>"
    else:
        if request.method=="POST":
            data=request.get_json()
            light=data["light"]
            update=Led(light,ID)
            update.update_state()
        return "testing"


@app.route('/channel/<int:ID>/api/get/humidifier/<string:apikey>',methods=["POST","GET"])
def getHumidifier(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        pass
    else:
        device=Humi("",ID)
        data=device.get_state()
        response=make_response(json.dumps(data))
        response.content_type="application/json"
        return response,200

@app.route('/channel/<int:ID>/api/post/humidifier/<string:apikey>',methods=["POST","GET"])
def postHumidifer(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        return "<h1>not found</h1>"
    else:
        if request.method=="POST":
            data=request.get_json()
            humidifier=data["humidifier"]
            update=Humi(humidifier,ID)
            update.update_state()
        return "Post completed!"
    
        


@app.route('/channel/<int:ID>/api/get/pump/<string:apikey>',methods=["POST","GET"])
def getPump(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        pass
    else:
        device=Pump("",ID)
        data=device.get_state()
        response=make_response(json.dumps(data))
        response.content_type="application/json"
        return response,200

@app.route('/channel/<int:ID>/api/post/pump/<string:apikey>',methods=["POST","GET"])
def postPump(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        return "<h1>not found</h1>"
    else:
        if request.method=="POST":
            data=request.get_json()
            pump=data["pump"]
            update=Pump(pump,ID)
            update.update_state()
        return "Post completed!"

@app.route('/channel/<int:ID>/api/get/water/<string:apikey>',methods=["POST","GET"])
def getWater(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        pass
    else:
        device=Water("",ID)
        data=device.get_state()
        response=make_response(json.dumps(data))
        response.content_type="application/json"
        return response,200

@app.route('/channel/<int:ID>/api/post/water/<string:apikey>',methods=["POST","GET"])
def postWater(ID,apikey):
    check=Users(ID,"","","",apikey)
    check=check.check_api()
    if check==False:
        return "<h1>not found</h1>"
    else:
        if request.method=="POST":
            data=request.get_json()
            water=data["water"]
            update=Water(water,ID)
            update.update_state()
        return "Post completed!"

@app.route('/logout')
def logout():
    session.pop("id",None)
    session.pop("api",None)
    return redirect(url_for("home"))




if __name__=="__main__":
    app.run(host='0.0.0.0',port=8090)