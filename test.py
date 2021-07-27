# For all intent and purpose, this is just a dummy file that will be used
# to test out new features on the webiste and mimick a request from the client to the server.
# This file may be subject to deletion if it proves unnecessary
from app import app
import unittest

class Test(unittest.TestCase):
    # Make sure setup is correct
    def testSetUp(self):
        test = app.test_client(self)
        resp = test.get('/login', content_type='html/text')
        self.assertEqual(resp.status_code, 200)

    # Make sure that login works correctly
    def testLogin(self):
        test = app.test_client(self)
        resp = test.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        self.assertIn(b'Welcome!', resp.data)
    
    # Make sure that putting in wrong credentials works
    def testBadLogin(self):
        test = app.test_client(self)
        resp = test.post(
            '/login',
            data=dict(username='something', password='somethingelse'),
            follow_redirects=True
        )
        self.assertIn(b'Sorry, unless you put the right info', resp.data)

    # Make sure that logging out works correctly
    def testLogOut(self):
        test = app.test_client(self)
        test.post(
            '/login',
            data=dict(username="admin", password="admin"),
            follow_redirects=True
        )
        resp = test.get('/logout', follow_redirects=True)
        self.assertIn(b'Goodbye, we will miss you!', resp.data)

    # Ensure that login is required
    def test_must_login(self):
        test = app.test_client(self)
        resp = test.get('/', follow_redirects=True)
        self.assertIn(b"view this page without logging in.", resp.data)

if __name__ == '__main__':
    unittest.main()