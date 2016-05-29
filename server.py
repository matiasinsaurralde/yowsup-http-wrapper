import tornado.ioloop
import tornado.web

from yowsup.layers import YowLayerEvent

class MainHandler(tornado.web.RequestHandler):
    def initialize(self, stack):
        self.stack = stack

    def get(self):
        self.stack.broadcastEvent(YowLayerEvent("sendMessage", dest='595981288424', msg='hello'))
        self.write("Hello, world")

def make_app(stack):
    return tornado.web.Application([
        (r"/", MainHandler, dict(stack=stack)),
    ])

# if __name__ == "__main__":
#     app = make_app()
#     app.listen(8888)
#    tornado.ioloop.IOLoop.current().start()
