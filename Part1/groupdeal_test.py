import os
import groupdeal
import unittest
import tempfile

class GroupDealTestCase(unittest.TestCase):

	def setUp(self):
		self.db_fd, groupdeal.app.config['DATABASE'] = tempfile.mkstemp()
		groupdeal.app.config['TESTING'] = True
		self.app = groupdeal.app.test_client()
		groupdeal.init_db()

	def tearDown(self):
		os.close(self.db_fd)
		os.unlink(groupdeal.app.config['DATABASE'])

	def login(self, username, password):
		return self.app.post('/login', data=dict(
			username = username,
			password = password
		), follow_redirects=True)

	def logout(self):
		return self.app.get('/logout', follow_redirects=True)

	def sign_up(self):
		return self.app.get('/sign_up', follow_redirects=True)

	def vendor_home(self):
		return self.app.get('/vendor_home', follow_redirects=True)
	
	def test_user(self):
		

	#def test_login_logout(self):
	#	rv = self.login('admin', 'default')
	#	assert 'You were logged in' in rv.data
	#	rv = self.logout()
	#	assert 'You were logged out' in rv.data
	#	rv = self.login('Robx', 'Chiarelli')
	#	assert 'Invalid username' in rv.data
	#	rv = self.login('Rob', 'Chiarellix')
	#	assert 'Invalid password' in rv.data




if __name__ == '__main__':
	unittest.main()
