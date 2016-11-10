from settings import dbsession, metadata, engine
from models import User, Company, Application, Country
from sqlalchemy.orm import joinedload
import bcrypt

class BaseRepository(object):
	def save(self, model):
		dbsession.add(model)
		dbsession.commit()
		return model

class UserRepository(BaseRepository):

	def bcrypt_password(self, password):
		return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(8))

	def find(self, email):
		return dbsession.query(User).filter(User.email == email).first()

	def find_login(self, email, password):
		user = self.find(email)
		if user and bcrypt.hashpw(password.encode('utf-8'), user.password) == user.password:
			return user

	def create(self, doc, name, email, tel, city_id, password):
		user = User(doc=doc, name=name, email=email, tel=tel, city_id=city_id, password=self.bcrypt_password(password))
		return self.save(user)

class CompanyRepository(BaseRepository):

	def create(self, name, tel, address, city_id, user_id):
		company = Company(name=name, tel=tel, address=address, city_id=city_id, user_id=user_id)
		return self.save(company)

class ApplicationRepository(BaseRepository):
 
	def find(self, id):
		return dbsession.query(Application).filter(Application.id == id).first()

	def create(self, name, amount, number_payments, company_id):
		application = Application(name=name, amount=amount, company_id=company_id, number_payments=number_payments, agree=None)
		return self.save(application)

	def agree(self, application, agree):
		application.agree = agree
		return self.save(application)

	def all_of_company(self, company):
		return dbsession.query(Application).filter(Application.company_id == company.id).options(joinedload('payments')).order_by(Application.id).all()

	def all_of_user(self, user):
		return self.all_of_company(user.company)
		
class CountryRepository(BaseRepository):

	def all(self):
		return dbsession.query(Country).options(joinedload('cities')).order_by(Country.id).all()