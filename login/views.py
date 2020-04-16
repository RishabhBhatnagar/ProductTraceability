from django.shortcuts import render, redirect
from django.urls import reverse
from collections import defaultdict
import datetime
import sys, os
CURR_PATH = os.path.abspath('./')
sys.path.insert(0, os.path.join(CURR_PATH, 'core'))
from core import db, blockchain


BC_FILE_PATH = 'bc_file'
bc = blockchain.Blockchain(BC_FILE_PATH, load_from_file=os.path.exists(BC_FILE_PATH))	
data_base = db.DataBase(os.path.join(CURR_PATH, db.DATABASE_FILE_NAME))



def login(req):
	uname = req.GET.get('uname')
	pswd = req.GET.get('psw')
	if uname is not None and pswd is not None and data_base.contains(uname + ' ' + pswd):
		with open('context', 'w') as fh:
			fh.write('{} {}'.format(uname, pswd))
		return render(req, 'actor.html', {})
	return render(req, 'login.html', dict(show_alert=1))

def home(req):
	return render(req, 'home.html', {})

def contact(req):
	return render(req, 'contact.html', {})

def about(req):
	return render(req, 'about.html')

def add_detail(req):
	return render(req, 'add_detail.html')

def view_details(req):
	return render(req, 'view_details.html')

def actor(req):
	return render(req, 'actor.html')

def timeline(req):
	with open('context') as fh:
		creds = fh.read()
	with open('file') as fh:
		lines = fh.read().split('\n')
	data = defaultdict(list)
	pname = ''
	data['pid'] = req.GET['pid']
	line = (line for line in lines if creds in line).__next__()
	role = line.split()[-1]
	for block in bc.chain[1:]:
		for tx in block.txs:
			tx_data = eval(tx['data'])
			if tx_data['pid'] == data['pid']:
				pname = max(pname, tx_data['pname'])
				timestamp = tx_data.get('timestamp', '')
				data[tx_data.get('role', 'other').lower()].append(timestamp + ' : ' + tx_data['desc'])
	data['pname'] = pname
	return render(req, 'timeline.html', data)

def signup(req):
	with open('file', 'a') as fh:
		print(req.GET)
		fh.write('{} {} {}\n'.format(req.GET['fname'], req.GET['pswd'], req.GET['actor']))
		return render(req, 'login.html', dict(show_alert=0, login_successful=1))

def product_detail_hander(req):
	with open('context') as fh:
		creds = fh.read()
	with open('file') as fh:
		lines = fh.read().split('\n')
	line = (line for line in lines if creds in line).__next__()
	role = line.split()[-1]
	data = dict(
		pid = req.GET['pid'],
		pname = req.GET['pname'],
		desc = req.GET['desc'],
		role = role,
		timestamp='%s' % datetime.datetime.now()
	)
	tx = blockchain.Transaction(data.__str__())
	bc.create_block([tx])
	return render(req, 'actor.html')