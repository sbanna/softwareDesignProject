# import stuff
import sqlite3
import os
import tempvariables
from contextlib import closing
from functools import wraps
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# create app
app = Flask(__name__)

# config
DATABASE = os.path.join(app.root_path, 'groupdeal_test.db')
# DATABASE = 'E:\git_repos\softwareDesignProject\Part1\groupdeal_test.db'
DEBUG = True
SECRET_KEY = 'development_key'
USERNAME = 'admin'
PASSWORD = 'default'

# login_required decorator (limits use of some functions to logged in users only)
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if g.user is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

app.config.from_object(__name__)

@app.route('/')
def home():
	return render_template('home.html')

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
@login_required
def vendor_home():
	return render_template('vendor_home.html')
	
@app.route('/sign_up')
def sign_up():
	return render_template('sign_up.html')
	
@app.route('/add_user', methods=['POST'])
def add_user():
	if (g.db.execute('select username from user_account')):
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
	return redirect(url_for('sign_up'))
	
@app.route('/create_product')
#@login_required
def create_product():
	return render_template("create_product.html")

@app.route('/add_product', methods = ['POST']) 
def add_product():
	g.db.execute('INSERT INTO product (product_name, price, image, description, vendor_id) \
				  values (?, ?, ?, ?, ?)',
				  (request.form['product_name'],
				   request.form['price'], 
				   request.form['image'], 
				   request.form['description'], 
				   request.form['vendor_id']))
	g.db.commit()
	flash("New product was added successfully")
	return render_template("create_product.html")
	
@app.route('/choose_product')
def choose_product():
	return render_template("choose_product.html")
	
@app.route('/show_product', methods = ['GET', 'POST'])
def show_product():
	product_qs = g.db.execute('SELECT product_id, price, image, description, vendor_id \
							   FROM product WHERE product_id = ?', 
							   [request.form['product_id']])
	product_info = []
	for i in product_qs:
		for j in i:
			product_info.append(j)
	return render_template("simpleCampaign.html",
							title = "GroupDeal Hoodie",
							description = product_info[3],
							currentPrice = product_info[1],
							nextPrice = "$40.00",
							amountContributers = 10,
							amountContriNeeded = 15,)
	
@app.route('/add_project')
def add_project():
	return render_template("add_project.html")
	
@app.route('/all_projects')
def all_projects():
	return render_template("all_projects.html", projects = tempvariables.all_projects)

@app.route('/edit_project')
def projectForm():
	return render_template("addproject.html", projects = tempvariables.all_projects)
							
@app.route('/pledge', methods = ['GET', 'POST'])
@login_required
def add_pledge():
	g.db.execute('INSERT INTO contributions (product_id, consumer_id, amount) values (?, ?, ?)',
				 [request.form['product_id'], request.form['consumer_id'], request.form['amount']])
	g.db.commit()
	flash("Pledge was successfully added")
	return redirect(url_for('simple_campaign'))

@app.route('/consumer_home')
@login_required
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
