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

logged_in = False
theName = ""

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
@app.route('/', methods=['GET'])
def all_projects():
	if not session['logged_in']:
		return render_template("all_projects.html", projects = tempvariables.all_projects)
	else:
		# this isn't done I need a contributions page and vender/customer func
		#user_campaigns_qs = g.db.execute('select campaign_name from campaign where')
		#projects = []
		#for p in tempvariables.all_projects:
		#	if p['']:
		#		print ""
		is_vendor = False
		campaigns = []
		cust_or_vend = g.db.execute('SELECT user_type FROM user_account WHERE username=? limit 1', [theName])
		rows = cust_or_vend.fetchall()
		for r in rows:
			if r[0] == 'vendor':
				is_vendor = True
		if is_vendor:
			for p in tempvariables.all_projects:
				if p['author'] == theName:
					campaigns.append(p)
		else:
			#user_campaigns_qs = g.db.execute('select campaign_name from campaign where')
			print "he's a consumer"
		return render_template("all_projects.html", projects = campaigns)

# MY VENDOR PAGE
# GETS ALL CAMPAIGNS MADE BY ME
@app.route('/vendor/me', methods = ['GET', 'POST'])
def my_campaigns():
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

# ADD A NEW PRODUCT
@app.route('/add_campaign')
def add_campaign():
	return render_template("add_project.html")


@app.route('/register', methods=['GET','POST'])
def register():
	global theName

	theusername = request.args.get('username')
	thepassword = request.args.get('password')
	checkmark = request.args.get('boolVendor') # this will either be 'vendor' or 'customer'

	account_exists = g.db.execute('select username from user_account where username=?', [theusername])
	rows = account_exists.fetchall()
	exists = 0
	for i in rows:
		if i[0] == theusername:
			print "username already exists"
			exists = 1
	if exists == 0:
		g.db.execute('INSERT INTO user_account (username, password, address, user_type) \
					 values (?, ?, ?, ?)',
					 [theusername, 
					  thepassword, 
					  '1234 Smith Street',
					  checkmark])
		g.db.commit()
		session['logged_in'] = True
		theName = theusername
	return redirect(url_for('all_projects'))

@app.route('/login', methods=['GET','POST'])
def login():
	global theName
	
	theusername = request.args.get('username')
	thepassword = request.args.get('password')

	account_exists = g.db.execute('select username from user_account where username=? and password=?', 
								  [theusername, thepassword])
	rows = account_exists.fetchall()
	if rows == []:
		exists = 0
	else:
		exists = 1

	# if things work set the below variable accordingly
	if exists:
		session['logged_in'] = True
		theName = theusername
	return redirect(url_for('all_projects'))

@app.route('/logout')
def logout():
	global theName

	session['logged_in'] = False
	theName = ""
	return redirect(url_for('all_projects'))

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
	file.close()

@app.route('/add_product', methods = ['POST']) 
def add_product():
	campaign_exists_qs = g.db.execute('SELECT * FROM campaign WHERE campaign_name=? AND vendor_name=?',
								   (request.form['campaign_name'],
									request.form['vendor_name'])
								  )
	campaign_exists = campaign_exists_qs.fetchall()
	if campaign_exists == []:
		print "This campaign already exists"
		return render_template("add_project.html")
	
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
	
@app.route('/campaign', methods=['GET'])
def campaign():
	campaign_name = request.args.get('name')
	vendor_name = request.args.get('vendor')
	curr_campaign = ""
	for i in tempvariables.all_projects:
		if i['title'] == campaign_name and i['author'] == vendor_name:
			curr_campaign = i
	return render_template("project.html", campaign = curr_campaign)
	
@app.route('/edit_project')
def projectForm():
	return render_template("add_project.html", projects = tempvariables.all_projects)

@app.route('/choose_product')
def choose_product():
	return render_template("choose_product.html")
	
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
		
#This is the login page
@app.route('/mylogin', methods = ['post','get'])
def login_page():
  global users
  #check to see if the users dictionary is empty, if it is read it in from the file
  if not bool(users): # if its empty, read it in from the file
    print "Reading in from the file"
    readUsers(users)

  # ck if the user is in the session
  if 'userName' in session:
    return redirect(url_for('homePage')) # simply just redirect to the homepage of the user
  # If the user sends back a request( either log in or create a new account)
  if request.method == 'POST':
    # ck which type of response it was
    if request.form["submit"] == "Sign In": # user is trying to log into his/her account
      print request.form["user_name"] #print to the console for debugging purposes
      userName = request.form["user_name"]
      password = (request.form["password"])
      # ck the credentials
      if checkCredentials(userName,password): #verification was a success
        # add it to the session, meaning we cache that the user is logged in. 
        # The user won't have to log back in
        session['userName'] = userName # basically a dictionary
        return redirect(url_for("homePage"))
      else:
        print "failed"
        return render_template("login.html", responsetext="You entered a invalid username/password")


    elif request.form["submit"] == "create_account":
      return redirect(url_for("create"))  # redirect to the users page
  return render_template("login.html")


# This is the create page
# Redirects here from the index page (AKA login page)
@app.route('/create/', methods = ['post', 'get'])
def create():
  global users
  if request.method == 'POST':
    #now get the name/username & password to create the account
    name = request.form['name'] # get the name
    userName = request.form['user_name'] # get User name
    password = request.form['password'] # get pass
    # check to see if this user_name exists because they must be unique!
    if users.has_key(userName):
      print "error key already exists"
      return render_template("create.html", responsetext = "User Name already taken :(")
    else:
      print "Key successfully created! "
      writeKey(users,name,userName,password) # write the key to the dictionary and to the file
      session['userName'] = userName
      # listStuff.insert(0,"")
      # followFriend("") 
      return redirect(url_for("login_page"))

  return render_template("create.html")

	
if __name__ == '__main__':
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' # this is the key used for the session
  	app.run("127.0.0.1",5000,debug = True)