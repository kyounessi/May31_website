from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import render_to_response
import pyramid.httpexceptions as exc

import mysql.connector as mysql
import os
import json
import requests


db_user = os.environ['MYSQL_USER']
db_pwd = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
db_host = os.environ['MYSQL_HOST']

def avatar(req):
    return render_to_response('templates/avatar.html',{},request = req)

def education(req):
    db = mysql.connect(host=db_host, passwd=db_pwd, user=db_user, database=db_name)
    cursor = db.cursor()
    cursor.execute("select school, degree, major, date from Mycreds;")
    my_record = cursor.fetchone()
    record = {
        "school": my_record[0],
        "degree": my_record[1],
        "major": my_record[2],
        "date": my_record[3]
    }
    return json.dumps(record)

def personal(req):
    db = mysql.connect(host=db_host, passwd=db_pwd, user=db_user, database=db_name)
    cursor = db.cursor()
    cursor.execute("select first_name, last_name, email from Users;")
    my_record = cursor.fetchone()
    record = {
        "first_name": my_record[0],
        "last_name": my_record[1],
        "email": my_record[2]
    }
    return json.dumps(record)

def project(req):
    db = mysql.connect(host=db_host, passwd=db_pwd, user=db_user, database=db_name)
    cursor = db.cursor()
    cursor.execute("select title, description, link, image_src from Projectdetails;")
    project_details = cursor.fetchone()
    cursor.execute("select URL from Teammembers;")
    team_details = cursor.fetchall()
    team_1 = team_details[0]
    team_2 = team_details[1]
    team_3 = team_details[2]
    #this section will probably experience errors
    record = {
        "title": project_details[0],
        "description": project_details[1],
        "link": project_details[2],
        "image_src": project_details[3],
        "team": {
            "Dong": team_1,
            "Anwar": team_2,
            "Isis": team_3
        }
    }
    return json.dumps(record)


def home(req):
    #ed_recs = requests.get(URL + "/education")
    #pers_recs = requests.get(URL + "/personal")
    #educations = []
    #educations.append(eds_recs['school'])
    #educations.extend([ed_recs['degree'],ed_recs['major'],ed_recs['date']])
    #print(educations)
    #personals = []
    #personals.append(pers_recs['first_name'])
    #personals.extend([pers_recs['last_name'], pers_recs['email']])
    #print(personals)
    
    #return render_to_response('templates/home.html', {'personals': personals, 'eds': educations}, request=req)
    return render_to_response('templates/home.html',{},request=req)

def welcome(req):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pwd)
    cursor = db.cursor()
    cursor.execute("select first_name, last_name, email, comment from Users;")
    records = cursor.fetchall()
    db.close()

    return render_to_response('templates/welcome.html', {'users': records}, request = req)

def about_us(req):
    return render_to_response('templates/aboutus.html',{}, request=req)

def cv(req):
    return render_to_response('templates/cv.html',{},request=req)

def save_info(info):
    db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pwd)
    cursor = db.cursor()
    query = "insert into Users (first_name, last_name, email, comment) values (%s, %s, %s, %s)"
    values = (info['f-name'], info['l-name'], info['emails'], info['comment'])
    cursor.execute(query, values)
    db.commit()
    db.close()


def add_info(req):
    new_info = req.POST.mixed()
    save_info(new_info)
    return render_to_response('templates/feedback.html',{},request=req)



if __name__ == '__main__':
    config = Configurator()

    config.include('pyramid_jinja2')
    config.add_jinja2_renderer('.html')

    config.add_route('home', '/')
    config.add_view(home, route_name= 'home')

    config.add_route('welcome', '/welcome')
    config.add_view(welcome, route_name = 'welcome')

    config.add_route('cv','/cv')
    config.add_view(cv, route_name = 'cv')

    config.add_route('avatar', '/avatar')
    config.add_view(avatar, route_name = 'avatar')

    config.add_route('personal', '/personal')
    config.add_view(personal, route_name = 'personal', renderer='json')

    config.add_route('education', '/education')
    config.add_view(education, route_name = 'education', renderer='json')

    config.add_route('project', '/project')
    config.add_view(project, route_name = 'project', renderer = 'json')

    config.add_route('about','/about')
    config.add_view(about_us, route_name = 'about')

    config.add_route('add_info', '/add_info')
    config.add_view(add_info, route_name = 'add_info', request_method = 'POST')


    config.add_static_view(name='/', path='./public', cache_max_age=3600)

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 4444, app)
    server.serve_forever()


