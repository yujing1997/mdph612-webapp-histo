import psycopg2

# PQSL Database Information
#DATABASE = "test_db"
#USER = "postgres"
#PASSWORD = "amilucy.2152ami"
#HOST = "127.0.0.1"
#PORT = "5432"

import psycopg2
import os
import pandas as pd

DATABASE = "mdph612yz"
USER = "postgres"
PASSWORD = "amilucy.2152ami"
HOST = "127.0.0.1"
PORT = "5432"

"""
This script builds all required database and populates them with mock data
"""

# create PATIENT_INFO database
con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD,
                       host=HOST, port=PORT)
print("Database opened successfully")


################ CREATE DATABASES ################


# Create patient database containing name and password
def create_patient_database(cur):
    cur.execute("DROP TABLE IF EXISTS PATIENT CASCADE")
    # create a table called PATIENT
    cur.execute('''CREATE TABLE PATIENT (
          PATIENTID INT PRIMARY KEY     NOT NULL,
          NAME           TEXT    NOT NULL,
          PASSWORD      TEXT     NOT NULL);''')
    

# Create image database containing image name and path
def create_image_database(cur):
    cur.execute("DROP TABLE IF EXISTS IMAGE CASCADE")
    cur.execute('''CREATE TABLE IMAGE (
          IMAGEID INT PRIMARY KEY     NOT NULL,
          NAME           TEXT    NOT NULL,
          FULLPATH            TEXT     NOT NULL);''')

# Create patient-image database linking images to patients
def create_patientimage_database(cur):
    cur.execute("DROP TABLE IF EXISTS PATIENT_IMAGE CASCADE")
    cur.execute('''CREATE TABLE PATIENT_IMAGE (
                PATIENTID INTEGER NOT NULL,
                IMAGEID INTEGER NOT NULL,
                PRIMARY KEY (PATIENTID , IMAGEID),
                FOREIGN KEY (PATIENTID)
                    REFERENCES PATIENT (PATIENTID)
                    ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (IMAGEID)
                    REFERENCES IMAGE (IMAGEID)
                    ON UPDATE CASCADE ON DELETE CASCADE
            )
        ''')
    
    
################ INSERT DATABASES ################

def insert_to_database(cur):
    # Patient information

    
    Patient_list = [
            [1, 'Yujing Jackson', 'Shirin'],
            [2, 'Marco DiFreddie', 'Piotr'],
            [3, 'Hossein Queen', 'Jan'],
            [4, 'Alexandru Mercury', 'Horacio']
            
        ]    

    # Image information
    Image_list = [
            [1, 'originalhisto','p1\A21.png'],
            [2, 'segmentation','p1\A21-annotation.png'],
            [3, 'histogram', 'p1\histogram1.png'],
            [4, 'originalhisto','p2\A42.png'],
            [5, 'segmentation','p2\A42-annotation.png'],
            [6, 'histogram', 'p2\histogram1.png'],
            [7, 'originalhisto','p3\A51.png'],
            [8, 'segmentation','p3\A51-annotation.png'],
            [9, 'histogram', 'p3\histogram1.png'],
            [10, 'originalhisto','p4\A52.png'],
            [11, 'segmentation','p4\A52-annotation.png'],
            [12, 'histogram', 'p4\histogram1.png'],
        ]
    
    # Patient-Image link
    patient_image = [
            [1,1],
            [1,2],
            [1,3],
            [2,4],
            [2,5],
            [2,6],
            [3,7],
            [3,8],
            [3,9],
            [4,10],
            [4,11],
            [4,12]
        ]
############ inserting data into created table ##########
    try:
        
        for row in Patient_list:
            cur.execute("INSERT INTO PATIENT (PATIENTID,NAME,PASSWORD) \
                VALUES (%i, '%s', '%s')"%(row[0],row[1],row[2]))
    except Exception as e:
        print (e)
        
    try:
        for row in Image_list:
            cur.execute("INSERT INTO IMAGE (IMAGEID,NAME,FULLPATH) \
                VALUES (%i, '%s', '%s')"%(row[0],row[1],row[2]))

    except Exception as e:
        print (e)
        
    try:
        for row in patient_image:
            cur.execute("INSERT INTO PATIENT_IMAGE (PATIENTID,IMAGEID) \
                VALUES (%i, %i)"%(row[0],row[1]))
    except Exception as e:
        print (e)


        
    ############### Querying data from database#######
    ################ DISPLAY DATABASES ################
def read_db(cur, table):
    cur.execute('SELECT * FROM %s'%table)
    rows = cur.fetchall()
    for row in rows:
        print (row)

def main():
    # Open Database
    con = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
    print("Database opened successfully")
    cur = con.cursor()

    # Create Database Tables
    create_patient_database(cur)
    create_image_database(cur)
    create_patientimage_database(cur)
    # create_organ_database(cur)
    # create_patientorgan_database(cur)

    # Insert data to tables
    insert_to_database(cur)
    con.commit()
    print("data inserted to database successfully")

    # Print Database Content
    #read_db(cur,'PATIENT')
    #read_db(cur, 'IMAGE')
    #read_db(cur, 'PATIENT_IMAGE')
    #read_db(cur, 'ORGAN')
    #read_db(cur, 'PATIENT_ORGAN')

if __name__ == "__main__":
    main()