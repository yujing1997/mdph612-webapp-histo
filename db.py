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

DATABASE = "mdph612yz2"
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
    

# Create  image database containing image name and path
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
            [4,'dicomslice','p1\dicom_png_test_001.png'],
            [5,'GTmask','p1\mask_png_test_001.png'],
            [6,'PREDmask','p1\pred_mask_test_001.png'],
            [7, 'originalhisto','p2\A42.png'],
            [8, 'segmentation','p2\A42-annotation.png'],
            [9, 'histogram', 'p2\histogram1.png'],
            [10,'dicomslice','p2\dicom_png_test_002.png'],
            [11,'GTmask','p2\mask_png_test_002.png'],
            [12,'PREDmask','p2\pred_mask_test_002.png'],
            [13, 'originalhisto','p3\A51.png'],
            [14, 'segmentation','p3\A51-annotation.png'],
            [15, 'histogram', 'p3\histogram1.png'],
            [16,'dicomslice','p3\dicom_png_test_003.png'],
            [17,'GTmask','p3\mask_png_test_003.png'],
            [18,'PREDmask','p3\pred_mask_test_003.png'],
            [19, 'originalhisto','p4\A52.png'],
            [20, 'segmentation','p4\A52-annotation.png'],
            [21, 'histogram', 'p4\histogram1.png'],
            [22,'dicomslice','p4\dicom_png_test_004.png'],
            [23,'GTmask','p4\mask_png_test_004.png'],
            [24,'PREDmask','p4\pred_mask_test_004.png'],
        ]
    
    # Patient-Image link: the first 3 images for each patient are histology-related, the latter 3 are dicom-related
    patient_image = [
            [1,1],
            [1,2],
            [1,3],
            [1,4],
            [1,5],
            [1,6],
            
            [2,7],
            [2,8],
            [2,9],
            [2,10],
            [2,11],
            [2,12],
            
            [3,13],
            [3,14],
            [3,15],
            [3,16],
            [3,17],
            [3,18],
            
            [4,19],
            [4,20],
            [4,21],
            [4,22],
            [4,23],
            [4,24],
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