"""
unitTest.py
====================
sample unit test framework
"""
#since the module is in testing folder, to make sure it finds __init__
#module, we need to run it using 
##################################
####python -m testing.unitTest####
##################################
#while in the application root directory ([some PATH]/TEAM-A3)
#further tests can be added in the file
import os
import unittest
from __init__ import application as app
from __init__ import db
 
 
TEST_DB = 'test.db'
 
 
class BasicTests(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(app.config['BASE_DIR'], 'database', TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
 
        # Disable sending emails during unit testing
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
 
if __name__ == "__main__":
    unittest.main()