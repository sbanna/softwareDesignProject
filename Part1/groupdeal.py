# import stuff
import sqlite3
import os
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# create app
app = Flask(__name__)

# config
# DATABASE = os.path.join(app.root_path, 'groupdeal_test.db')
DATABASE = 'E:\git_repos\softwareDesignProject\Part1\groupdeal_test.db'
DEBUG = True
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'default'

app.config.from_object(__name__)

@app.route('/')
def home():
	return render_template('index.html')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)
	
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
	
@app.route('/vendor_home')
def vendor_home():
	return render_template('vendor_home.html')
	
@app.route('/add_user', methods=['POST'])
def add_user():
	if (g.db.execute('select username from user_account'):
		flash('This username is already in use.')
	else:
		g.db.execute('INSERT INTO user_account (username, password, address) \
					 values (?, ?, ?)',
					 [request.form['username'], 
					  request.form['password'], 
					  request.form['address']])
		if (request.form['type'] == 'consumer'):
			g.db.execute('INSERT INTO consumer_account (username) values (?)',
						 [request.form['username']])
		else:
			g.db.execute('INSERT INTO vendor_account (username) values (?, ?)',
						 [request.form['username']])
		g.db.commit()
		flash("New user was successfully added")
	return redirect(url_for('add_user'))
	
@app.route('/add_product', method=['POST'])
def add_product():
	g.db.execute('INSERT INTO product (price, image, description, vendor_id) \
				  values (?, ?, ?, ?)'
				 [request.form['price'], request.form['image'], 
				  request.form['description'], request.form['vendor_id']])
	g.db.commit()
	flash("New product was successfully added")
	return redirect(url_for('add_product'))

@app.route('/consumer_home')
def consumer_home():
	return render_template('consumer_home.html')

def connect_db():
	return sqlite3.connect(app.config['DATABASE'])
	
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
		
@app.before_request
def before_request():
	g.db = connect_db()
	
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()
	
if __name__ == '__main__':
	app.run()