# import stuff
import sqlite3
import os
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# create app
app = Flask(__name__)
app.config.from_object(__name__)

# config
DATABASE = os.path.join(app.root_path, 'groupdeal.db')
DEBUG = True
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'default'

@app.route('/')
def home():
	return render_template('index.html')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
	
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
	
if __name__ == '__main__':
	app.run()