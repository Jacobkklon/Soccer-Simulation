#Only running this 1 time to initialize the required DB information
import mysql.connector

#Connecting to my DB hosted on AWS RDS MYSQL DB
mydb = mysql.connector.connect(
    host ="rds-mysql-soccer-project.cnuykwkwidxt.us-east-1.rds.amazonaws.com",
    user ="admin",
    password ="JacobKlonsky")

#First we must create the DB (#NOTE - this was a nice exercise but I realized it isn't needed because I already have a DB)
# mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE soccer_sim")


#Then we connect to the DB
mydb = mysql.connector.connect(
    host = "rds-mysql-soccer-project.cnuykwkwidxt.us-east-1.rds.amazonaws.com",
    user = "admin",
    password = "JacobKlonsky",
    database="RDS_MySQL_Soccer_Project")

