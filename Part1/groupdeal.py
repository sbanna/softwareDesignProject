# import stuff
import sqlite3
import os
import tempvariables
import fileinput
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

# THIS IS THE HOME PAGE
# GETS ALL CAMPAIGNS, STORES IN projects VARIABLE 
@app.route('/')
def all_projects():
	return render_template("all_projects.html", projects = tempvariables.all_projects)

# VENDOR PAGE
# GETS ALL CAMPAIGNS BY vender_name
@app.route('/vendor/<string:vendor_name>', methods = ['GET', 'POST'])
def vendor_campaigns(vendor_name):
	return render_template("all_projects.html", projects = tempvariables.all_projects)

# MY PAGE
# GETS ALL PROJECTS THAT I PLEDGED
@app.route('/my_pledges', methods = ['GET', 'POST'])
def my_pledges():
	return render_template("all_projects.html", projects = tempvariables.all_projects)

@app.route('/add_campaign')
def add_campaign():
	return render_template("add_project.html")



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
	
def write_to_file(name, price, image_str, descr, descr_simple, num_pledges, vendor, price_2 = 'n/a'):
	dict = "\t\t{\r\t\t\t'image':'%s',\
			\r\t\t\t'title':'%s',\
			\r\t\t\t'author':'%s',\
			\r\t\t\t'shortDescription':'%s',\
			\r\t\t\t'currentPrice':%s,\
			\r\t\t\t'amountCommitted':%s,\
			\r\t\t\t'daysLeft':99,\
			\r\t\t\t'nextPrice':%s,\
			\r\t\t\t'nextCommitAmount':99,\
			\r\t\t\t'percentCommitted':99,\
			\r\t\t},\r" % (image_str,name,vendor,descr_simple,price,num_pledges, price_2)
	file = open('Part1/tempvariables.py', 'r+')
	contents = file.readlines()
	file.close()
	
	contents.insert(13, dict)
	
	file = open('Part1/tempvariables.py', 'w')
	contents = "".join(contents)
	file.write(contents)
	file.close();

@app.route('/add_product', methods = ['POST']) 
def add_product():
	g.db.execute('INSERT INTO campaign (campaign_name, price, image, descr, descr_simple, num_pledges, vendor_name) \
				  values (?, ?, ?, ?, ?, ?, ?)',
				  (request.form['campaign_name'],
				   request.form['price_1'], 
				   request.form['image'], 
				   request.form['descr'], 
				   request.form['descr_simple'], 
				   0, 
				   request.form['vendor_name']))
	g.db.commit()
	
	write_to_file(request.form['campaign_name'],
				   request.form['price_1'], 
				   request.form['image'], 
				   request.form['descr'], 
				   request.form['descr_simple'], 
				   0, 
				   request.form['vendor_name'],
				   request.form['price_2'])
	
	#get the id of the campaign we just created
	campaign_qs = g.db.execute('SELECT campaign_id FROM campaign ORDER BY campaign_id DESC LIMIT 1')
	campaign = ""
	for i in campaign_qs:
		for j in i:
			campaign = j
	
	#this doesn't work.  dunno why
	if (request.form['price_2']):
		g.db.execute('INSERT INTO price_points (campaign_id, pledge_num, new_price) VALUES (?, ?, ?)',
					 (campaign, "100", request.form['price_2']))
					 
	if (request.form['price_3']):
		g.db.execute('INSERT INTO price_points (campaign_id, pledge_num, new_price) VALUES (?, ?, ?)',
					 (campaign, "200", request.form['price_3']))
	
	if (request.form['price_4']):
		g.db.execute('INSERT INTO price_points (campaign_id, pledge_num, new_price) VALUES (?, ?, ?)',
					 (campaign, "300", request.form['price_4']))
					 
	if (request.form['price_5']):
		g.db.execute('INSERT INTO price_points (campaign_id, pledge_num, new_price) VALUES (?, ?, ?)',
					 (campaign, "400", request.form['price_5']))
	
	if (request.form['price_6']):
		g.db.execute('INSERT INTO price_points (campaign_id, pledge_num, new_price) VALUES (?, ?, ?)',
					 (campaign, "500", request.form['price_6']))
	
	g.db.commit()
	
	flash("New product was added successfully")
	return render_template("add_project.html")
	
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

@app.route('/campaign')
def campaign():
	return render_template("project.html")
	
@app.route('/edit_project')
def projectForm():
	return render_template("add_project.html", projects = tempvariables.all_projects)
							
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
