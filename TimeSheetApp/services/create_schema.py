from flask import Blueprint, render_template, session, redirect, url_for, escape, request, flash
import pymysql
#from services.config import database_config as db_conf

db_conf = {
'user': 'root',
'password': '',
'host': 'localhost',
'db_name': 'inventory_db'
}
db = pymysql.connect(db_conf['host'], db_conf['user'], db_conf['password'], db_conf['db_name'])

cursor = db.cursor()
sql = '''CREATE TABLE users (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(350) NOT NULL,
       email VARCHAR(80) NOT NULL,
       password VARCHAR(50) NOT NULL,
       user_type ENUM('SA','A','U') DEFAULT 'U',
       is_active ENUM('Yes', 'No') DEFAULT 'Yes'
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
cursor.execute(sql)

"""sql = '''CREATE TABLE emp_personal (
       id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(350) NOT NULL,
       ph1 INT(10) NOT NULL,
       ph2 INT(10) DEFAULT NULL,
       blood_group VARCHAR(4) DEFAULT NULL,
       address VARCHAR(3999) NOT NULL,
       emergency_contact_no INT(10) NOT NULL,
       gender ENUM('Male','Female') NOT NULL,
       email VARCHAR(80) NOT NULL,
       dob DATE NOT NULL
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
cursor.execute(sql)"""

sql = '''CREATE TABLE emp_details (
       id INT AUTO_INCREMENT PRIMARY KEY,
      name VARCHAR(350) NOT NULL,
      ph1 BIGINT(10) NOT NULL,
      ph2 BIGINT(10) DEFAULT NULL,
      blood_group VARCHAR(4) DEFAULT NULL,
      address VARCHAR(3999) NOT NULL,
      emergency_contact_no BIGINT(10) NOT NULL,
      gender ENUM('Male','Female') NOT NULL,
      email VARCHAR(80) NOT NULL,
      dob DATE NOT NULL,
       start_date DATE NOT NULL,
       end_date DATE DEFAULT NULL,
       is_active ENUM('Yes', 'No') NOT NULL,
       employee ENUM('Yes', 'No') NOT NULL,
       hra FLOAT(10,2) DEFAULT '0.00',
       lta FLOAT(10,2) DEFAULT '0.00',
       uniform_allowance FLOAT(10,2) DEFAULT '0.00',
       edu_allowance FLOAT(10,2) DEFAULT '0.00',
       softfurnishing_allowance FLOAT(10,2) DEFAULT '0.00',
       years FLOAT(10,2) DEFAULT '0.00',
       food_coupon ENUM('Yes', 'No') DEFAULT 'No',
       days INT(6) DEFAULT 0,
       vichle_engno VARCHAR(30) DEFAULT NULL
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
cursor.execute(sql)

sql = '''CREATE TABLE projects (
       id INT AUTO_INCREMENT PRIMARY KEY,
       project_code VARCHAR(40) NOT NULL,
       project_name VARCHAR(80) NOT NULL,
       client VARCHAR(90) NOT NULL,
       client_code VARCHAR(40) NOT NULL,
       status ENUM('Not Started', 'Active', 'Hold', 'Cancelled', 'Completed', 'Proposal') DEFAULT 'Not Started',
       progress INT(3) DEFAULT 0,
       start_date DATE NOT NULL,
       end_date DATE DEFAULT NULL,
       biling_contact VARCHAR(50),
       bill_to_email VARCHAR(50),
       about VARCHAR(210)
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
cursor.execute(sql)

sql = '''CREATE TABLE project_emp (
       id INT AUTO_INCREMENT PRIMARY KEY,
       emp_name VARCHAR(350) NOT NULL,
       emp_email VARCHAR(80) NOT NULL,
       is_active ENUM('Yes', 'No') NOT NULL,
       start_date DATE NOT NULL,
       end_date DATE,
       project_code VARCHAR(40) NOT NULL
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
cursor.execute(sql)

sql = '''CREATE TABLE emp_work (
       id INT AUTO_INCREMENT PRIMARY KEY,
       emp_name VARCHAR(250) NOT NULL,
       project_name VARCHAR(200) NOT NULL,
       project_code VARCHAR(40) NOT NULL,
       hours INT(4) NOT NULL,
       email VARCHAR(80) NOT NULL,
       start_date DATE NOT NULL,
       end_date DATE NOT NULL,
       summary LONGTEXT NOT NULL,
       detail_summary LONGTEXT NOT NULL
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
cursor.execute(sql)

sql = '''INSERT INTO users (id, name, email, password, user_type) VALUES
(0, 'Natraj Gujran', 'natraj@nichesoft.net', 'natraj@nichesoft.net', 'SA') '''

cursor.execute(sql)
cursor.close()
db.close()
