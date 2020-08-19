#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   This file contains routines and classes used to read and write data from the database

"""
import psycopg2   #  postgres I/O lib



#   This class is used to read and write data to database
class db:

    
    #   create dictionary of {exposed store, physical table} names 
    #   client reference the exposed name and this class access the physical name


    # Connection to postgresql database
    __conn = ""
    __cur = ""

    # initialize this object
    def __init__(self, db_host, db_path, db_user, db_password):
        self.dbHost = db_host
        self.dbPath = db_path
        self.dbUser = db_user
        self.dbPassword = db_password

    
    def connect(self):
        connectStr = "host=" + self.dbHost \
            + " dbname=" + self.dbPath  \
            + " user=" + self.dbUser \
            + " password=" + self.dbPassword
        print(connectStr)
        self.__conn =  psycopg2.connect(connectStr)
        # Open Cursor to perform DB ops
        self.__cur = self.__conn.cursor()
                            


       

    #  data write method 
   # def __execute__(timestamp, table, json_data):
 
    # def __retrieve(timestamp, table):
    #     return "NYI"

    # def __update(timestamp, table, json_data):
    #     return "NYI"

    # def __delete(timestamp, table):
    #     return "NYI"

    # exposed methods
    # def add(timestamp, store, json_data):
    #     __add__(timestamp, storage[store], json_data)
    def add(self, timestamp, store, json_data):
        columns =  '"PollTime", "DataSource", "JsonData"'  #   replace with column parameter
        #sql = '"INSERT INTO ' + '"PollData"' + " (" + columns + ") VALUES ( %s, %s, %s)"
        #print(sql)
        sql = 'INSERT INTO "PollData" ( "PollTime", "DataSource", "JsonData") VALUES ( %s, %s, %s)'
        data = (timestamp, store, json_data)
    #    data = ( store, json_data)
        self. __cur.execute(sql, data)
        self.__conn.commit()



