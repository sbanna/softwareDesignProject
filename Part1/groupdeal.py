# import stuff
import sqlite3
import os
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
	
if __name__ == '__main__':
	app.run()