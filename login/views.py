from django.shortcuts import render
import sys, os
CURR_PATH = os.path.abspath('./')
sys.path.insert(0, os.path.join(CURR_PATH, 'core'))
from core import db


data_base = db.DataBase(os.path.join(CURR_PATH, db.DATABASE_FILE_NAME))


def login(req):
	uname = req.GET.get('uname')
	pswd = req.GET.get('psw')
	if uname is not None and pswd is not None:
		if data_base.contains(uname + ' ' + pswd):
			return render(req, 'actor.html', {})
	return render(req, 'login.html', dict(show_alert='true'))

def home(req):
	return render(req, 'home.html', {})

def contact(req):
	return render(req, 'home.html', {})

def about(req):
	return render(req, 'about.html')

def add_detail(req):
	return render(req, 'add_detail.html')

def view_details(req):
	return render(req, 'view_details.html')

def actor(req):
	return render(req, 'actor.html')

def timeline(req):
	return render(req, 'timeline.html')