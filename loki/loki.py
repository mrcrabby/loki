import tornado.httpserver
import tornado.ioloop
import tornado.web


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/plain")
        self.write("You are getting atom feed")



application = tornado.web.Application([
              (r'/', MainHandler)])

if __name__ == '__main__':
    server = tornado.httpserver.HTTPServer(application)
    server.listen(9999)
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        print "\nStopping the server..."
        tornado.ioloop.IOLoop.instance().stop()
