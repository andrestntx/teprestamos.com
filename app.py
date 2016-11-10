import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
import uuid
import bcrypt

from sqlalchemy.orm import joinedload
from models import Country, Application
from settings import dbsession, metadata, engine
from tornado.options import define, options, parse_command_line
from repositories import UserRepository, CompanyRepository, ApplicationRepository, CountryRepository

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="run in debug mode")


class BaseHandler(tornado.web.RequestHandler):
    user_repository = UserRepository()
    application_repository = ApplicationRepository()
    country_repository = CountryRepository()
    company_repository = CompanyRepository()

    def get_user(self): 
        return self.user_repository.find(self.get_secure_cookie("user"))

class MainHandler(BaseHandler):
    def get(self): 
    	if(self.get_secure_cookie("user")):
            user = self.get_user()
            app = self.application_repository.all_of_user(user)
            self.render("applications.html", applications=app, user=user)

    	self.redirect("/login")


class ApplicationHandler(BaseHandler):
    def get(self):
        if(self.get_secure_cookie("user")):
            app = dbsession.query(Application).options(joinedload('payments')).filter(Application.id == self.get_argument("show")).first()
            self.render("application.html", application=app, user=self.get_user())

        self.redirect("/login")

    def post(self):
        if(self.get_secure_cookie("user")):
            user = self.get_user()
            application = self.application_repository.create(self.get_argument("name", ""), self.get_argument("amount", ""), self.get_argument("number_payments", ""), user.company.id)

            self.redirect("/application?show=" + `application.id`)
        self.redirect("/login")

class ApplicationAgreeHandler(BaseHandler):
    def post(self):
        application = self.application_repository.find(self.get_argument("application", ""))

        if(application):
            self.application_repository.agree(application, self.get_argument("agree", None))
            self.write({'success': True, 'agree_state': application.agree_state})
        else:
            self.write({'success': False})


class RegisterHandler(BaseHandler):
    def get(self):
        if self.get_secure_cookie("user"):
            self.redirect("/")
        else:
            countries = self.country_repository.all()
            self.render("auth/register.html", countries=countries)

    def post(self):
        user = self.user_repository.find(self.get_argument("email", ""))

        if user:
            error_msg = u"?error=" + tornado.escape.url_escape("Login name already taken")
            self.redirect(u"/login" + error_msg)

        user = self.user_repository.create(self.get_argument("doc", ""), self.get_argument("name", ""), self.get_argument("email", ""), self.get_argument("tel", ""), self.get_argument("city_id", ""), self.get_argument("password", ""))
        company = self.company_repository.create(self.get_argument("company_name", ""), self.get_argument("company_tel", ""), self.get_argument("company_address", ""), self.get_argument("company_city_id", ""), user.id)

        self.set_secure_cookie("user", user.email)
        self.redirect("/")


class LoginHandler(BaseHandler):
    def get(self):
        if self.get_secure_cookie("user"):
            self.redirect("/")
        else:
            self.render("auth/login.html")

    def post(self):
        user = self.user_repository.find_login(self.get_argument("email", ""), self.get_argument("password", ""))

        if user:
            self.set_secure_cookie("user", user.email)
            self.redirect("/")
        else:
            self.set_secure_cookie('flash', "Login incorrect")
            self.redirect("/login")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("user")
        self.redirect("/login")


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
        	(r"/application", ApplicationHandler),
            (r"/application/agree", ApplicationAgreeHandler),
	        (r'/login', LoginHandler),
	        (r'/register', RegisterHandler),
	        (r'/logout', LogoutHandler)
        ],
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        debug=options.debug,
    )
    ##metadata.create_all(engine)
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
