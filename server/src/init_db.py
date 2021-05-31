import mysql.connector as mysql
import os
from dotenv import load_dotenv
load_dotenv('credentials.env')

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST'] 


db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
cursor = db.cursor()


cursor.execute("drop table if exists Users;")


try:
  cursor.execute("""
    CREATE TABLE Users (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      first_name  VARCHAR(30) NOT NULL,
      last_name   VARCHAR(30) NOT NULL,
      email       VARCHAR(50) NOT NULL,
      comment    VARCHAR(50) NOT NULL,
      created_at  TIMESTAMP
    );
  """)
except:
  print("Users table already exists. Not recreating it.")

cursor.execute("drop table if exists Mycreds;")

try:
  cursor.execute("""
    CREATE TABLE Mycreds (
      id      integer  AUTO_INCREMENT PRIMARY KEY,
      school  VARCHAR(30) NOT NULL,
      degree  VARCHAR(30) NOT NULL,
      major   VARCHAR(50) NOT NULL,
      date    VARCHAR(4) NOT NULL
    );
  """)
except:
  print("Mycreds table already exists. Not recreating it.")

cursor.execute("drop table if exists Projectdetails;")

try:
  cursor.execute("""
    CREATE TABLE Projectdetails (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      title       VARCHAR(50) NOT NULL,
      description VARCHAR(1000) NOT NULL,
      link        VARCHAR(200) NOT NULL,
      image_src   VARCHAR(200) NOT NULL
    );
  """)
except:
  print("Projectdetails table already exists.")

cursor.execute("drop table if exists Teammembers;")

try:
  cursor.execute("""
    CREATE TABLE Teammembers(
      id    integer AUTO_INCREMENT PRIMARY KEY,
      name  VARCHAR(10) NOT NULL,
      URL   VARCHAR(100) NOT NULL
    );
  """)
except:
  print("Teammembers table already exists.")

add_user = "insert into Users (first_name, last_name, email, comment, created_at) values (%s, %s, %s, %s, %s)"
add_creds = "insert into Mycreds (school, degree, major, date) values (%s, %s, %s, %s)"
add_details = "insert into Projectdetails (title, description, link, image_src) values (%s, %s, %s, %s)"
add_team = "insert into Teammembers (name, URL) values (%s, %s)"
value_user = [
  ('Kasra', 'Younessi', 'kyouness@ucsd.edu', 'ECE is cool', '2021-05-15 12:00:00')
]
value_creds = [
  ('UCSD', 'Bachelor of Science', 'Machine Learning and control', '2021')
]
value_details = [
  ('Team Big Brains Smartdoor', 'A smartdoor that uses latest technological features in machine learning and web serving to improve convenience and quality of life', 'http://comingsoon', 'https://cdn3.vectorstock.com/i/1000x1000/76/42/smart-door-lock-icon-simple-style-vector-26987642.jpg')
]
value_team = [
  ('Dong', '128.199.15.251'),
  ('Anwar', 'coming.soon'),
  ('Isis', '64.227.107.46')
]
cursor.executemany(add_user, value_user)
cursor.executemany(add_creds, value_creds)
cursor.executemany(add_details, value_details)
cursor.executemany(add_team, value_team)

db.commit()
print('---------- DATABASE INITIALIZED ----------')
cursor.close()
db.close()




