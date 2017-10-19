import os
import json
import datetime
import psycopg2
import psycopg2.extras
import tornado.httpserver
import tornado.ioloop
import tornado.web


conn = psycopg2.connect( database="todo", user="", password="", host="localhost", port=5432)
cur = conn.cursor()


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('index.html')


class AboutHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('about.html')


class ContactHandler(tornado.web.RequestHandler):

    def get(self):
        self.render('contact.html')


    def post(self):

        name = self.get_argument('name')
        email = self.get_argument('email')
        message = self.get_argument('message')
        created = datetime.datetime.now()

        query = "INSERT INTO contact (name, email, message, created_on) VALUES (%s, %s, %s, %s)"
        cur.execute(query, (name, email, message, created))
        conn.commit()

        self.write('Submitted successfully')




def main():

    settings = dict(
        cookie_secret=str(os.urandom(45)),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
        autoreload=True,
        gzip=True,
        debug=True,
        login_url='/login',
        autoescape=None
    )

    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/about", AboutHandler),
        (r"/contact", ContactHandler)
    ], **settings)

    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    main()
