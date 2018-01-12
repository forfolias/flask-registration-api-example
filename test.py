import os
import unittest
from project import app, db

TEST_DB = 'test.db'


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                                            TEST_DB)
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    # executed after each test
    def tearDown(self):
        pass

    ###############
    #### tests ####
    ###############

    def test_invalid_url(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 404)

    def test_invalid_registration_missing_name(self):
        response = self.register("", "george@vasilakos.com")
        self.assertEqual(response.status_code, 422)

    def test_invalid_registration_missing_email(self):
        response = self.register("george", "")
        self.assertEqual(response.status_code, 422)

    def test_invalid_registration_invalid_email(self):
        response = self.register("george", "george")
        self.assertEqual(response.status_code, 422)

    def test_valid_registration(self):
        response = self.register("george", "george@vasilakos.com")
        self.assertEqual(response.status_code, 200)

    def test_invalid_registration_user_exists(self):
        self.register("george", "george@vasilakos.com")
        response = self.register("george", "george@vasilakos.com")
        self.assertEqual(response.status_code, 422)

    def register(self, name, email):
        return self.app.post(
            '/register',
            data=dict(name=name, email=email),
            follow_redirects=True
        )


if __name__ == "__main__":
    unittest.main()
