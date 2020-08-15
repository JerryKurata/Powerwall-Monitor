#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   This file contains routines and classes used to read and write data from the database

"""



#   This class is used to read and write data to database
class db:

    
    #   create dictionary of {exposed store, physical table} names 
    #   client reference the exposed name and this class access the physical name
    storage = {
        'state_of_charge', 'charge_state'
    }

    def __init__(self):
       

    #  data write method 
    def __add(timestamp, table, json_data):
        return "NYI"

    def __retrieve(timestamp, table):
        return "NYI"

    def __update(timestamp, table, json_data):
        return "NYI"

    def __delete(timestamp, table):
        return "NYI"

    # exposed methods
    def add(timestamp, store, json_data):
        __add(timestamp,storage[store], json_data)



