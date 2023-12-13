from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from flask import send_file
import numpy as np
import cv2
import threading
import os
import time
import shutil
import hashlib
import imagehash
import PIL.Image
from PIL import Image
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="question_generator"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'

@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM sb_user where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            result=" Your Logged in sucessfully**"
            return redirect(url_for('staff_home')) 
        else:
            result="Your logged in fail!!!"
        

    return render_template('index.html',msg=msg,act=act)

@app.route('/index_admin',methods=['POST','GET'])
def index_admin():
    cnt=0
    act=""
    msg=""
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM sb_admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            session['username'] = username1
            result=" Your Logged in sucessfully**"
            return redirect(url_for('view_ins')) 
        else:
            result="You are logged in fail!!!"
        

    return render_template('index_admin.html',msg=msg,act=act)



@app.route('/view_ins', methods=['GET', 'POST'])
def view_ins():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_user order by id")
    value = mycursor.fetchall()

    act = request.args.get('act')
    if act=="del":
        did = request.args.get('did')
        mycursor.execute("delete from sb_user where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_ins')) 
    
    return render_template('view_ins.html', data=value)

@app.route('/add_dept', methods=['GET', 'POST'])
def add_dept():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_department order by id")
    value = mycursor.fetchall()

    act = request.args.get('act')

    if request.method=='POST':
        
        dept=request.form['dept']
        detail=request.form['detail']
        mycursor.execute("SELECT count(*) FROM sb_department where dept=%s",(dept, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM sb_department")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO sb_department(id, dept, detail) VALUES (%s, %s, %s)"
            val = (maxid, dept, detail)
            act="success"
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
            return redirect(url_for('add_dept')) 

        
    if act=="del":
        did = request.args.get('did')
        mycursor.execute("delete from sb_department where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_dept')) 
    
    return render_template('add_dept.html', data=value)

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_department order by id")
    value = mycursor.fetchall()
    
    mycursor.execute("SELECT * FROM sb_subject order by id")
    data = mycursor.fetchall()

    act = request.args.get('act')

    if request.method=='POST':
        
        dept=request.form['dept']
        semester=request.form['semester']
        sub_code=request.form['sub_code']
        subject=request.form['subject']
        
        mycursor.execute("SELECT max(id)+1 FROM sb_subject")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO sb_subject(id, dept, semester, sub_code, subject) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid, dept, semester, sub_code, subject)
        act="success"
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "record inserted.")
        return redirect(url_for('add_subject')) 

        
    if act=="del":
        did = request.args.get('did')
        mycursor.execute("delete from sb_subject where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_subject')) 
    
    return render_template('add_subject.html', data=data, value=value)

@app.route('/view_subject', methods=['GET', 'POST'])
def view_subject():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_department order by id")
    value = mycursor.fetchall()
    
    data=[]

    act = request.args.get('act')

    if request.method=='POST':
        
        dept=request.form['dept']
        semester=request.form['semester']
        mycursor.execute("SELECT * FROM sb_subject where dept=%s && semester=%s",(dept, semester))
        data = mycursor.fetchall()
        
        
    if act=="del":
        did = request.args.get('did')
        mycursor.execute("delete from sb_subject where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_subject')) 
    
    return render_template('view_subject.html', data=data, value=value)


@app.route('/add_mark', methods=['GET', 'POST'])
def add_mark():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_mark order by id")
    data = mycursor.fetchall()
    


    act = request.args.get('act')

    if request.method=='POST':
        
        mark=request.form['mark']
        
        mycursor.execute("SELECT max(id)+1 FROM sb_mark")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO sb_mark(id, mark) VALUES (%s, %s)"
        val = (maxid, mark)
        act="success"
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "record inserted.")
        return redirect(url_for('add_mark')) 

        
    if act=="del":
        did = request.args.get('did')
        mycursor.execute("delete from sb_mark where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_mark')) 
    
    return render_template('add_mark.html', data=data)

@app.route('/add_question', methods=['GET', 'POST'])



@app.route('/view_question', methods=['GET', 'POST'])
def view_question():
    msg=""
    sid=request.args.get("sid")
    mycursor = mydb.cursor()
    data2=[]
    mycursor.execute("SELECT * FROM sb_mark order by id")
    value = mycursor.fetchall()
    
    mycursor.execute("SELECT * FROM sb_subject where id=%s",(sid,))
    data = mycursor.fetchone()
    dept=data[1]
    sem=data[3]
  
    

    act = request.args.get('act')

    if request.method=='POST':
        
        mark=request.form['mark']
        kl=request.form['kl']
        co=request.form['co']
        mycursor.execute("SELECT * FROM sb_question where subject_id=%s",(sid,))
        data2 = mycursor.fetchall()
        
        
    if act=="del":
        did = request.args.get('did')
        mycursor.execute("delete from sb_question where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_question',sid=sid)) 
    
    return render_template('view_question.html', msg=msg, data=data, value=value, dept=dept, sem=sem, sid=sid,data2=data2)

@app.route('/reg_ins',methods=['POST','GET'])
def reg_ins():
    result=""
    act=""
    mycursor = mydb.cursor()
    
    
    if request.method=='POST':
        
        uname=request.form['uname']
        name=request.form['name']        
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']        
        pass1=request.form['pass']

        
        now = datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        mycursor = mydb.cursor()

        mycursor.execute("SELECT count(*) FROM sb_user where uname=%s",(uname, ))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM sb_user")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            sql = "INSERT INTO sb_user(id, name, mobile, email, location,  uname, pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (maxid, name, mobile, email, location, uname, pass1)
            act="success"
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "record inserted.")
           
        else:
            act="wrong"
            result="Already Exist!"
    return render_template('reg_ins.html',act=act,result=result)



@app.route('/staff_home', methods=['GET', 'POST'])
def staff_home():
    uname=""
    st=""
    if 'username' in session:
        uname = session['username']
    name=""
    data=[]
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_user where uname=%s",(uname, ))
    value = mycursor.fetchone()
    
    mycursor.execute("SELECT distinct(dept) FROM sb_department")
    value1 = mycursor.fetchall()

    if request.method=='POST':        
        dept=request.form['dept']
        sem=request.form['semester']

        mycursor.execute("SELECT count(*) FROM sb_subject where dept=%s && semester=%s",(dept, sem))
        cn = mycursor.fetchone()[0]
        if cn>0:
            st="1"
            mycursor.execute("SELECT * FROM sb_subject where dept=%s && semester=%s",(dept, sem))
            data = mycursor.fetchall()
        
    return render_template('staff_home.html',value=value, value1=value1,data=data,st=st)


@app.route('/staff_paper', methods=['GET', 'POST'])
def staff_paper():
    uname=""
    st=""
    if 'username' in session:
        uname = session['username']
    name=""
    data=[]
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_user where uname=%s",(uname, ))
    value = mycursor.fetchone()

    mycursor.execute("SELECT * FROM sb_paper order by id desc")
    data = mycursor.fetchall()

    return render_template('staff_paper.html',value=value,data=data,st=st)
    
@app.route('/staff_gen', methods=['GET', 'POST'])
def staff_gen():
    msg=""
    uname=""
    st=""
    act=request.args.get("act")
    sid=request.args.get("sid")
    if 'username' in session:
        uname = session['username']
    name=""
    data=[]
    uname="SS1"
    
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_user where uname=%s",(uname, ))
    value = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM sb_subject where id=%s",(sid,))
    value1 = mycursor.fetchone()
    semester=value1[3]
    dept=value1[1]
    scode=value1[4]
    subject=value1[2]

    if request.method=='POST':        
        set_num=request.form['set_num']
        test=request.form['test']
        regulation=request.form['regulation']
        year=request.form['year']
        sem=request.form['sem']
        edate=request.form['edate']
        time_hours=request.form['time_hours']
        max_mark=request.form['max_mark']

        mycursor.execute("SELECT max(id)+1 FROM sb_paper")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        edd=edate.split("-")
        ed=edd[2]+"-"+edd[1]+"-"+edd[0]
        
        sql = "INSERT INTO sb_paper(id,uname,sid,dept,semester,scode,subject,set_num,test,regulation,year,sem,edate,time_hours,max_mark) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,uname,sid,dept,semester,scode,subject,set_num,test,regulation,year,sem,ed,time_hours,max_mark)
        msg="success"
        mycursor.execute(sql, val)
        mydb.commit()

    if act=="del":
        did = request.args.get('did')
        mycursor.execute("delete from sb_paper where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('staff_gen',sid=sid))

    
    mycursor.execute("SELECT * FROM sb_paper order by id desc")
    data = mycursor.fetchall()
        
    return render_template('staff_gen.html',msg=msg,value=value,data=data,act=act)

@app.route('/staff_ques', methods=['GET', 'POST'])
def staff_ques():
    msg=""
    uname=""
    st=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    sid=request.args.get("sid")
    if 'username' in session:
        uname = session['username']
    name=""
    data=[]
    uname="SS1"
    num=0
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_user where uname=%s",(uname, ))
    value = mycursor.fetchone()

    mycursor.execute("SELECT * FROM sb_mark order by mark")
    vmark = mycursor.fetchall()
    
    mycursor.execute("SELECT * FROM sb_subject where id=%s",(sid,))
    value1 = mycursor.fetchone()
    semester=value[3]
    dept=value1[1]
    scode=value1[4]
    subject=value1[2]

    if request.method=='POST':        
        part=request.form['part']
        num_ques=request.form['num_ques']
        qmark=request.form['qmark']
        qtype=request.form['qtype']

        '''if qorder=="Double":
            num=int(num_ques)*2
        else:
            num=int(num_ques)'''
        num=int(num_ques)
        if qtype=="1":
            mycursor.execute("SELECT count(*) FROM sb_question where subject_id=%s && mark=%s order by rand()",(sid, qmark))
            dd = mycursor.fetchone()[0]
            if dd>=num:
                st="1"
                
                mycursor.execute("SELECT max(id)+1 FROM sb_paper_ques")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1

                
                
                sql = "INSERT INTO sb_paper_ques(id,uname,sid,pid,part,num_ques,qmark,qtype) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (maxid,uname,sid,pid,part,num_ques,qmark,'1')
                msg="success"
                mycursor.execute(sql, val)
                mydb.commit()
                #########
                dt=[]
                mycursor.execute("SELECT * FROM sb_question where subject_id=%s && mark=%s order by rand()",(sid, qmark))
                dd2 = mycursor.fetchall()

                mycursor.execute("SELECT count(*) FROM sb_paper_ques2 where pid=%s",(pid,))
                rowno = mycursor.fetchone()[0]

                
                i=0
                for ds in dd2:
                    if i<num:
                        rowno+=1
                        dt.append(str(ds[0]))
                        mycursor.execute("SELECT max(id)+1 FROM sb_paper_ques2")
                        maxid2 = mycursor.fetchone()[0]
                        if maxid2 is None:
                            maxid2=1
                        sql = "INSERT INTO sb_paper_ques2(id,uname,sid,pid,partid,qid,question,mark,kl,co,qtype,value1) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
                        val = (maxid2,uname,sid,pid,str(maxid),ds[0],ds[7],ds[4],ds[5],ds[6],qtype,rowno)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        i+=1
                print(dt)
                #qs=",".join(dt)
            else:
                st="2"

        else:
            mycursor.execute("SELECT max(id)+1 FROM sb_paper_ques")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
            
            sql = "INSERT INTO sb_paper_ques(id,uname,sid,pid,part,num_ques,qmark,qtype) VALUES (%s, %s, %s, %s, %s, %s, %s,%s)"
            val = (maxid,uname,sid,pid,part,num_ques,qmark,'2')
            msg="success"
            mycursor.execute(sql, val)
            mydb.commit()

            mycursor.execute("SELECT count(*) FROM sb_paper_ques2 where pid=%s",(pid,))
            rowno = mycursor.fetchone()[0]
                
            i=1
            while i<=num:
                rowno+=1
                mycursor.execute("SELECT max(id)+1 FROM sb_paper_ques2")
                maxid2 = mycursor.fetchone()[0]
                if maxid2 is None:
                    maxid2=1

                sql = "INSERT INTO sb_paper_ques2(id,uname,sid,pid,partid,qtype,value1) VALUES (%s, %s, %s, %s, %s, %s,%s)"
                val = (maxid2,uname,sid,pid,maxid,qtype,rowno)
                mycursor.execute(sql, val)
                mydb.commit()
                i+=1
            


    mycursor.execute("SELECT * FROM sb_paper_ques where pid=%s",(pid,))
    dd = mycursor.fetchall()
    for ds in dd:
        dt=[]
        dt.append(ds[0])
        dt.append(ds[1])
        dt.append(ds[2])
        dt.append(ds[3])
        dt.append(ds[4])
        dt.append(ds[5])
        dt.append(ds[6])
        dt.append(ds[7])
        i=1
        dt3=[]
        dt4=[]
        if ds[7]==1:
            mycursor.execute("SELECT * FROM sb_paper_ques2 where partid=%s",(ds[0],))
            dd2 = mycursor.fetchall()
            for ds2 in dd2:
                dt2=[]
                dt2.append(ds2[5])
                dt2.append(ds2[6])
                dt3.append(dt2)
                i+=1
            dt.append(dt3)
        else:
           
            numq=ds[5]
            i=1
            mycursor.execute("SELECT * FROM sb_paper_ques2 where partid=%s",(ds[0],))
            dd2 = mycursor.fetchall()
            for ds2 in dd2:
                dt21=[]
                
                dt21.append(ds2[0])

                dt5=[]
                mycursor.execute("SELECT * FROM sb_paper_ques3 where ques_id=%s",(ds2[0],))
                dd3 = mycursor.fetchall()
                for ds3 in dd3:
                    dt51=[]
                    dt51.append(ds3[6])
                    dt51.append(ds3[7])
                    dt51.append(ds3[10])
                    dt5.append(dt51)

                dt21.append(dt5)
                i+=1

                dt4.append(dt21)
            dt.append(dt4)
            
        
        data.append(dt)



        
    if act=="del":
        did = request.args.get('did')
        mycursor.execute("delete from sb_paper_ques3 where partid=%s",(did,))
        mydb.commit()
        mycursor.execute("delete from sb_paper_ques2 where partid=%s",(did,))
        mydb.commit()
        mycursor.execute("delete from sb_paper_ques where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('staff_ques',pid=pid,sid=sid)) 
        
    return render_template('staff_ques.html',msg=msg,act=act,value=value,data=data,sid=sid,pid=pid,st=st,vmark=vmark)

@app.route('/staff_sub', methods=['GET', 'POST'])
def staff_sub():
    msg=""
    uname=""
    st=""
    act=request.args.get("act")
    pid=request.args.get("pid")
    sid=request.args.get("sid")
    partid=request.args.get("partid")
    rid=request.args.get("rid")
    if 'username' in session:
        uname = session['username']
    name=""
    data=[]
    uname="SS1"
    num=0
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sb_user where uname=%s",(uname, ))
    value = mycursor.fetchone()

    mycursor.execute("SELECT * FROM sb_mark order by mark")
    vmark = mycursor.fetchall()
    
    mycursor.execute("SELECT * FROM sb_subject where id=%s",(sid,))
    value1 = mycursor.fetchone()
    semester=value[3]
    dept=value1[1]
    scode=value1[4]
    subject=value1[2]

    rnw=['i','ii','iii','iv','v','vi','vii','viii','ix','x']

    if request.method=='POST':        
        
        qorder=request.form['qorder']
        num_ques=request.form['num_ques']
        qmark=request.form['qmark']
        num=int(num_ques)
        mycursor.execute("SELECT count(*) FROM sb_question where subject_id=%s && mark=%s order by rand()",(sid, qmark))
        dd = mycursor.fetchone()[0]
        if dd>=num:
            st="1"
            dt=[]
            mycursor.execute("SELECT * FROM sb_question where subject_id=%s && mark=%s order by rand()",(sid, qmark))
            dd2 = mycursor.fetchall()
            i=0
            dq=[]
            for ds1 in dd2:
                mycursor.execute("SELECT * FROM sb_paper_ques3 where partid=%s",(partid,))
                sq = mycursor.fetchall()
                a=0
                for sr in sq:
                    if ds1[0]==sr[5]:
                        a+=1
                if a==0:
                    dq.append(str(ds1[0]))
            dqq=len(dq)
            if dqq>=num:
                vu1=""
                vu2=""
                vu3=""
                for ds2 in dq:
                    if i<num:
                        mycursor.execute("SELECT * FROM sb_question where id=%s",(ds2,))
                        ds = mycursor.fetchone()

                        mycursor.execute("SELECT max(id)+1 FROM sb_paper_ques3")
                        maxid2 = mycursor.fetchone()[0]
                        if maxid2 is None:
                            maxid2=1

                        ###
                        if qorder=="A":
                            mycursor.execute("SELECT count(*) FROM sb_paper_ques3 where qorder='A' && ques_id=%s",(rid,))
                            bs1 = mycursor.fetchone()[0]
                            if bs1==0:
                                vu1=str(rid)
                                vu2="a"
                            if bs1==1:
                                vu1=""
                                vu2="ii"
                                mycursor.execute("update sb_paper_ques3 set value2='a i' where qorder='A' && value1=%s",(str(rid),))
                                mydb.commit()
                            if bs1>1:
                                vu=""
                                if bs1<10:
                                    vu2=rnw[bs1]
                                else:
                                    vu2=""
                        ##
                        else:
                            mycursor.execute("SELECT count(*) FROM sb_paper_ques3 where qorder='B' && ques_id=%s",(rid,))
                            bs2 = mycursor.fetchone()[0]
                            if bs2==0:
                                vu1=""
                                vu2="b"
                                vu3="yes"
                            if bs2==1:
                                vu1=""
                                vu2="ii"
                                mycursor.execute("update sb_paper_ques3 set value2='b i' where qorder='B' && value3='yes'")
                                mydb.commit()
                            if bs2>1:
                                vu=""
                                if bs2<10:
                                    vu2=rnw[bs2]
                                else:
                                    vu2=""
                        ##

                        sql = "INSERT INTO sb_paper_ques3(id,uname,sid,pid,partid,qid,question,mark,kl,co,qorder,ques_id,value1,value2,value3) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s)"
                        val = (maxid2,uname,sid,pid,partid,ds[0],ds[7],ds[4],ds[5],ds[6],qorder,rid,vu1,vu2,vu3)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        
                        '''mycursor.execute("SELECT max(id)+1 FROM sb_paper_ques2")
                        maxid2 = mycursor.fetchone()[0]
                        if maxid2 is None:
                            maxid2=1
                        sql = "INSERT INTO sb_paper_ques2(id,uname,sid,pid,partid,qid,question,mark,kl,co,qorder,ques_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        val = (maxid2,uname,sid,pid,partid,ds[0],ds[7],ds[4],ds[5],ds[6],qorder,rid)
                        mycursor.execute(sql, val)
                        mydb.commit()'''
                        i+=1
                msg="success"
            else:
                st="2"
        else:
            st="2"

    return render_template('staff_sub.html',msg=msg,act=act,value=value,data=data,sid=sid,pid=pid,st=st,vmark=vmark)


@app.route('/view_paper', methods=['GET', 'POST'])
def view_paper():
    msg=""
    uname=""
    st=""
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="",
      charset="utf8",
      database="question_generator"
    )
    
    data2=[]
    act=request.args.get("act")
    pid=request.args.get("pid")
    sid=request.args.get("sid")
    if 'username' in session:
        uname = session['username']

    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT * FROM sb_paper where id=%s",(pid,))
    data = mycursor.fetchone()
    sid=data[2]
    dept=data[3]

    mycursor.execute("SELECT * FROM sb_department where dept=%s",(dept,))
    value1 = mycursor.fetchone()

    #mycursor.execute("SELECT * FROM sb_subject where dept=%s",(dept,))
    #value1 = mycursor.fetchone()
    
    mycursor.execute("SELECT * FROM sb_paper_ques where pid=%s",(pid,))
    dd2 = mycursor.fetchall()

    k=0

    for ds2 in dd2:
        dt=[]

        dt.append(ds2[0])
        dt.append(ds2[1])
        dt.append(ds2[2])
        dt.append(ds2[3])
        dt.append(ds2[4])
        dt.append(ds2[5])
        dt.append(ds2[6])
        dt.append(ds2[7])

        mycursor.execute("SELECT * FROM sb_paper_ques2 where partid=%s",(ds2[0],))
        val1 = mycursor.fetchall()
        dt1=[]
        
        for v1 in val1:
            k+=1
            
            dt2=[]
            dt2.append(v1[0])
            dt2.append(v1[1])
            dt2.append(v1[2])
            dt2.append(v1[3])
            dt2.append(v1[4])
            dt2.append(v1[5])
            dt2.append(v1[6])
            dt2.append(v1[7])
            dt2.append(v1[8])
            dt2.append(v1[9])
            dt2.append(v1[10])
            dt2.append(v1[11])
            dt4=[]
            if v1[10]==2:

               
                
                mycursor.execute("SELECT * FROM sb_paper_ques3 where ques_id=%s order by ques_id,qorder",(v1[0],))
                val2 = mycursor.fetchall()
                for v2 in val2:
                    dt3=[]
                    dt3.append(v2[0])
                    dt3.append(v2[1])
                    dt3.append(v2[2])
                    dt3.append(v2[3])
                    dt3.append(v2[4])
                    dt3.append(v2[5])
                    dt3.append(v2[6])
                    dt3.append(v2[7])
                    dt3.append(v2[8])
                    dt3.append(v2[9])
                    dt3.append(v2[10])
                    dt3.append(v2[11])
                    dt3.append(v2[12])
                    dt3.append(v2[13])
                    dt3.append(v2[14])

                    dt4.append(dt3)
                
                dt2.append(dt4)
            dt1.append(dt2)

            
            '''mycursor.execute("SELECT * FROM sb_paper_ques3 where ques_id=%s",(v1[0],))
            val2 = mycursor.fetchall()
            for v2 in val2:
                dt3=[]
                dt3.append(v2[0])
                dt3.append(v2[1])
                dt3.append(v2[2])
                dt3.append(v2[3])
                dt3.append(v2[4])
                dt3.append(v2[5])
                dt3.append(v2[6])
                dt3.append(v2[7])
                dt3.append(v2[8])
                dt3.append(v2[9])
                dt3.append(v2[10])
                dt3.append(v2[11])

                dt2.append(dt3)'''
            
            
            

        dt.append(dt1)
        

        tot=ds2[5]*ds2[6]
        dt.append(str(tot))
        data2.append(dt)
        

    return render_template('view_paper.html',msg=msg,act=act,sid=sid,pid=pid,data=data,data2=data2,value1=value1)





@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
