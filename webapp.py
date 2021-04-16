# -*- coding: utf-8 -*-
"""
creating a web application, main code

@author: Yujing Zou 
"""
from flask import Flask, render_template, session
from flask import  request, Response, session, redirect, g, url_for
# from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
import io
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pathlib

# current path directory of the parent folder 
parentDir = str(pathlib.Path().absolute())

# PQSL Database Information
DATABASE = "mdph612yz"
USER = "postgres"
PASSWORD = "amilucy.2152ami"
HOST = "127.0.0.1"
PORT = "5432"

# Configure Folders/Flask
IMAGE_FOLDER = parentDir + '\\static'

app = Flask(__name__, template_folder='templates')
app.secret_key = 'ilovemj'

app.config['IMAGE_FOLDER'] = IMAGE_FOLDER
app.config["DEBUG"] = True


# app = Flask(__name__)

# db = SQLAlchemy(app)

# Redirect root page to login
    # can input the staff usename and password
    # re-direct to the /selectpatient page
@app.route('/')
def start():
    return redirect('http://127.0.0.1:5000/stafflogin')

# Redirect root page to selecting a patient
@app.route('/stafflogin',methods=['GET','POST'])
def stafflogin():
    error = None
    
    if request.method == 'POST':
        if request.form['username'] != 'Yujing Zou' or request.form['password'] != 'ilovemichaeljackson':
            error = 'Invalid credentials. Please try again! :-)'
        else:
            # return redirect('http://127.0.0.1:5000/select_patient')
            return redirect(url_for('select_patient'))

        
    return render_template('stafflogin.html', error=error)
    # return render_template('login2.html', error=error)
    # return redirect('http://127.0.0.1:5000/select_patient')
    
    


# Selecting a patient page
    # can input patient username and password and login
    # will re-direct to the main home page
@app.route('/select_patient', methods=['GET', 'POST'])
def select_patient():
    error = None
    
    
    if request.method == 'POST':
        # Get username and password input by user
        p_name = request.form['username']
        password = request.form['password']
        
        #connect to the database
        try:        
            conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
        except:
            print("I am unable to connect to the database")
        # Query all patients from database
        # query_patient = "SELECT patient.patient_id, patient.name, patient.password FROM PATIENT"
        query_patient = """SELECT PATIENT.PATIENTID, PATIENT.NAME, PATIENT.PASSWORD FROM PATIENT"""
    
        #cursor
        cur = conn.cursor()
        
        cur.execute(query_patient)
        
        results_patient =cur.fetchall()

        # See if name exists in database and if password matches
        for i in range(len(results_patient)):
            # Both name and password match, redirect to description page
            if p_name == results_patient[i][1] and password == results_patient[i][2]:
                # Save patient id and name as session variables
                session['p_id'] = i+1
                session['p_name'] = p_name 
                error = None
                return redirect('http://127.0.0.1:5000/home')

            # Name exists but wrong password
            if p_name == results_patient[i][1] and not password == results_patient[i][2]:
                error = 'Invalid Password. Please try again.'
                break

            # Name doesn't exist in file
            else:
                error = 'The name you entered does not exist. Please try again.'

    return render_template('login.html', error=error)
    #return render_template('selectpatient.html', error=error)
        # selectpatient.html worked with the css and js scratched from online, but here we keep using login.html
        # to because the login button works.

# Load main Home page
    # after choosing a patient, 3 images will display on this page
        # the original histogathological image, the segmented version and the nuclei size distribution
@app.route('/home',  methods=['GET', 'POST'])
# def load_patient():
def load_oriimg():
    error = None
    
    # get current user's patientID and name
    p_id = session.get('p_id', None)
    print(p_id)
    p_name = session.get('p_name', None)
    print(p_name)
    
    # get the three images linked to patient in current session from database
    if p_id != "":
        query_img = """SELECT IMAGE.IMAGEID, IMAGE.NAME, IMAGE.FULLPATH FROM IMAGE 
            INNER JOIN PATIENT_IMAGE ON IMAGE.IMAGEID=PATIENT_IMAGE.IMAGEID 
            WHERE PATIENT_IMAGE.PATIENTID=%s"""%(p_id)
        # query_dicom
        
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD,host=HOST,port=PORT)
        cur = conn.cursor()
        cur.execute(query_img)
        results_img = cur.fetchall()
        
        
    else:
        results_img = []
    
    print(results_img)    
    
    print(str(results_img[0][2]))
    print(str(results_img[1][2]))
    print(str(results_img[2][2]))

    # specify file name
    #full_filename = os.path.join(app.config['IMAGE_FOLDER'], results_img)
    # full_filename = app.config['IMAGE_FOLDER'] + '\\'+ str(results_img[0][2])
    # print(full_filename)
    # full_filename = "\static\p2\A42-annotation.png"
    # full_filename = "\static\p2\histogram1.png"  
    # full_filename = "\static\p1\A21.png"
    
    ori_filename = '\\static\\'+ str(results_img[0][2]) # showing the original histopathological image
    #seg_filename = '\\static\\'+ str(results_img[1][2]) # segmented histopathological image
    #histogram_filename = '\\static\\'+ str(results_img[2][2]) # nuclei size distibution histogram 

    print(ori_filename)
    # display the unsegmeented version first, then segmented, then the histogram distribution 

    return render_template("home.html", user_image = ori_filename
                           ,row_img = results_img
                           ,p_id = p_id
                           ,p_name = p_name
                           )

    
    
    
    # return render_template('home.html', error=error), results_img, p_id, p_name
            
@app.route('/home-segment',  methods=['GET', 'POST'])
def load_segimg():
    error = None

    # get current user's patientID and name
    p_id = session.get('p_id', None)
    print(p_id)
    p_name = session.get('p_name', None)
    print(p_name)
    
    # get the three images linked to patient in current session from database
    if p_id != "":
        query_img = """SELECT IMAGE.IMAGEID, IMAGE.NAME, IMAGE.FULLPATH FROM IMAGE 
            INNER JOIN PATIENT_IMAGE ON IMAGE.IMAGEID=PATIENT_IMAGE.IMAGEID 
            WHERE PATIENT_IMAGE.PATIENTID=%s"""%(p_id)
        # query_dicom
        
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD,host=HOST,port=PORT)
        cur = conn.cursor()
        cur.execute(query_img)
        results_img = cur.fetchall()
        
        
    else:
        results_img = []
    
    print(results_img); print(str(results_img[0][2])); print(str(results_img[1][2])); print(str(results_img[2][2]))

    # specify filename
    
    # ori_filename = '\\static\\'+ str(results_img[0][2]) # showing the original histopathological image
    seg_filename = '\\static\\'+ str(results_img[1][2]) # segmented histopathological image
    #histogram_filename = '\\static\\'+ str(results_img[2][2]) # nuclei size distibution histogram 

    print(seg_filename)

    return render_template("home-segment.html", user_image = seg_filename
                           ,row_img = results_img
                           ,p_id = p_id
                           ,p_name = p_name
                           )

    return render_template('home-segment.html',error = error)

@app.route('/home-cellinfo',  methods=['GET', 'POST'])
def load_cellinfo():
    error = None

    # get current user's patientID and name
    p_id = session.get('p_id', None)
    print(p_id)
    p_name = session.get('p_name', None)
    print(p_name)
    
    # get the three images linked to patient in current session from database
    if p_id != "":
        query_img = """SELECT IMAGE.IMAGEID, IMAGE.NAME, IMAGE.FULLPATH FROM IMAGE 
            INNER JOIN PATIENT_IMAGE ON IMAGE.IMAGEID=PATIENT_IMAGE.IMAGEID 
            WHERE PATIENT_IMAGE.PATIENTID=%s"""%(p_id)
        # query_dicom
        
        conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD,host=HOST,port=PORT)
        cur = conn.cursor()
        cur.execute(query_img)
        results_img = cur.fetchall()
        
        
    else:
        results_img = []
    
    print(results_img); print(str(results_img[0][2])); print(str(results_img[1][2])); print(str(results_img[2][2]))

    # specify filename
    
    # ori_filename = '\\static\\'+ str(results_img[0][2]) # showing the original histopathological image
    # seg_filename = '\\static\\'+ str(results_img[1][2]) # segmented histopathological image
    histogram_filename = '\\static\\'+ str(results_img[2][2]) # nuclei size distibution histogram 

    print(histogram_filename)

    return render_template("home-cellinfo.html", user_image = histogram_filename
                           ,row_img = results_img
                           ,p_id = p_id
                           ,p_name = p_name
                           )

    return render_template('home-segment.html',error = error)


# @app.route('/')
# def index():
#     return "<h1 style=' color: red'>Hello Flask! </h1>"



if __name__ == '__main__':
    app.run(debug=True)
    