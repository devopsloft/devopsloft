#!/usr/bin/python

###########################################################
#
# This python script is used for mysql database backup
#
# Written by : Yariv Klonover
# Created date:  28/11/2018
# Script Revision: 0.1
#
##########################################################

# Import required python libraries

import os
import time
import datetime
import pipes

# MySQL database details to which backup to be done. A user having enough privileges should be defined.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databases names one on each line and assigned to DB_NAME variable.

DB_HOST = 'localhost'
DB_USER = 'root'
DB_USER_PASSWORD = '12345'
#DB_NAME = '/backup/dbnameslist.txt' preperation for multiple db backup
DB_NAME = 'devopsloft'
BACKUP_PATH = '/backup/dbbackup'

# Getting current DateTime to create the separate backup folder like "20180817-123433".
# DATETIME = time.strftime('%Y%m%d-%H%M%S')
# TODAYBACKUPPATH = BACKUP_PATH + '/' + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
# try:
#     os.stat(TODAYBACKUPPATH)
# except:
#     os.mkdir(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
# print ("checking for databases names file.")
# if os.path.exists(DB_NAME):
#     file1 = open(DB_NAME)
#     multi = 1
#     print ("Databases file found...")
#     print ("Starting backup of all dbs listed in file " + DB_NAME)
# else:
#     print ("Databases file not found...")
#     print ("Starting backup of database " + DB_NAME)
#     multi = 0

# Starting actual database backup process.
# if multi:
#    in_file = open(DB_NAME,"r")
#    in_file.close()
#    p = 1

dbfile = open(DB_NAME,"r")
flength = len(in_file.readlines())
 
   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(dumpcmd)
       gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(gzipcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(dumpcmd)
   gzipcmd = "gzip " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(gzipcmd)

print ("")
print ("Backup script completed")
print ("Your backups have been created in '" + TODAYBACKUPPATH + "' directory")
