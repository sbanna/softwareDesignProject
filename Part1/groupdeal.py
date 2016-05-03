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

# ADD A NEW PRODUCT
@app.route('/add_campaign')
def add_campaign():
	return render_template("add_project.html")

@app.route('/campaign')
def campaign():
	return render_template("project.html",project = tempvariables.campaign)



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


users = {} # this holds all the users Stored as {userid, {username,password}}

#Verify whether the user entered the user_id and password correctly
def checkCredentials(userName,typedPass):
  global users 
  if users.has_key(userName):
    (name,userPass) = users[userName]
    return (typedPass == userPass)
  else:
    return False

# read the users from the file
def readUsers(users):
  # so read the file and store all the users in the dictionary
  file = open("users.txt","r") #open file for only reading
  for line in file:
    string  = line.split(':') # split the line based on colon (:). (name userId )
    i = 0
    while i < len(string): #loop through the file and read in the users
      name = string[i]
      i+=1
      user_name = string[i]
      i+= 1
      password = string[i].strip("\n")
      i+=1
      users[user_name] = (name,password)
  print (users)
  file.close()

#When we successfully create a user, insert into the dictionary and write to the file
def writeKey(users,name,userName,password):
  users[userName] = (name,password) #insert into the dictionary
  file = open("users.txt","a") #write to the file
  line = name + ":"+userName+":"+password+"\n"
  file.write(line)
  file.close()
  # also make a blank entry for the user tweets and friend list
  userTweets[userName] = []
  userFriends[userName] = []
	
if __name__ == '__main__':
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT' # this is the key used for the session
  	app.run("127.0.0.1",5000,debug = True)
