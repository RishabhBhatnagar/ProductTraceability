from django.shortcuts import render
import sys, os
CURR_PATH = os.path.abspath('./')
sys.path.insert(0, os.path.join(CURR_PATH, 'core'))
from core import db


data_base = db.DataBase(os.path.join(CURR_PATH, db.DATABASE_FILE_NAME))


def login(req):
	if data_base.contains(req.GET['uname'] + ' ' + req.GET['pswd']):
		return render(req, 'next.html', {})
	return render(req, 'login.html', dict(show_alert='true'))
