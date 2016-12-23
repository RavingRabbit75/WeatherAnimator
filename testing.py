from app import app
from project import db
from project.users.models import User
import unittest
from flask_testing import TestCase
# from flask_wtf.csrf import CsrfProtect


# CsrfProtect(app)

class BaseTestCase(TestCase):
	def create_app(self):
		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///testing.db"
		app.config['WTF_CSRF_ENABLED'] = False
		return app

	def setUp(self):
		db.create_all()
		person1=User("imp@gmail.com", "bumbum", "Tyrion", "Lannister")
		person2=User("superman@gmail.com", "lois", "Clark", "Kent")
		db.session.add_all([person1, person2])
		db.session.commit()


	def tearDown(self):
		db.drop_all()


	def test_render(self):
		response = self.client.get("/", content_type="html/text")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Enter location to see weather.", response.data)


	def test_create(self):
		response=self.client.post(
			"/users/signup",
			data=dict(email="new@gmail.com", password="somepassword", confirm_password="somepassword", first_name="Dirty", last_name="BumBum"),
			follow_redirects=True
		)
		self.assertIn(b"Dirty BumBum", response.data)



if __name__ == "__main__":
	unittest.main()