import datetime
from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, Sequence, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from settings import Base


class Application(Base):
	__tablename__ = 'applications'

	commercial_state_rejected = 0
	commercial_state_approved = 1
	commercial_state_pending = 2

	id = Column(Integer, Sequence('application_id_seq'), primary_key=True)
	company_id = Column(ForeignKey('companies.id'))
	agree = Column(Integer)
	amount = Column(Integer)
	name = Column(String(50))
	number_payments = Column(Integer)

	payments = relationship("Payment", back_populates="application")
	company = relationship("Company", back_populates="applications")

	@hybrid_property
	def is_approved(self):
		return self.commercial_state == self.commercial_state_approved

	@hybrid_property
	def agree_state(self):
		if self.is_approved:
			if self.agree == 1:
				return 'Si'
			elif self.agree == 0:
				return 'No'

			return 'Pendiente'

		return '-'

	@hybrid_property
	def commercial_state(self):
		if(self.amount < 1000000):
			return self.commercial_state_pending
		elif(self.amount <= 10000000):
			return self.commercial_state_approved
		
		return self.commercial_state_rejected

	@hybrid_property
	def commercial_state_text(self):
		if(self.commercial_state == self.commercial_state_pending):
			return "Pendiente"
		elif(self.commercial_state == self.commercial_state_approved):
			return "Aprobado"

		return "Rechazado"

	@hybrid_property
	def count_payments(self):
		return len(self.payments)

class City(Base):
	__tablename__ = 'cities'

	id = Column(Integer, Sequence('city_id_seq'), primary_key=True)
	contry_id = Column(ForeignKey('contries.id'))
	name = Column(String(50))

	country = relationship("Country", back_populates="cities")
	companies = relationship("Company", back_populates="city")
	users = relationship("User", back_populates="city")


class Company(Base):
	__tablename__ = 'companies'

	id = Column(Integer, Sequence('company_id_seq'), primary_key=True)
	city_id = Column(ForeignKey('cities.id'))
	user_id = Column(ForeignKey('users.id'))
	address = Column(String(50))
	name = Column(String(50))
	tel = Column(String(50))

	applications = relationship("Application", back_populates="company")
	city = relationship("City", back_populates="companies")
	user = relationship("User", back_populates="company", uselist=False)


class Country(Base):
	__tablename__ = 'contries'

	id = Column(Integer, Sequence('country_id_seq'), primary_key=True)
	name = Column(String(50))

	cities = relationship("City", back_populates="country")
	

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, Sequence('payment_id_seq'), primary_key=True)
    application_id = Column(ForeignKey('applications.id'))
    value = Column(Integer)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    application = relationship("Application", back_populates="payments")		
	

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
	city_id = Column(ForeignKey('cities.id'))
	doc = Column(BigInteger)
	email = Column(String(50))
	name = Column(String(50))
	password = Column(String(255))
	tel = Column(String(50))

	city = relationship("City", back_populates="users")
	company = relationship("Company", back_populates="user", uselist=False)


