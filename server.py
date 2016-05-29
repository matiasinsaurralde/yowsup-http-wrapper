import tornado.ioloop
import tornado.web
from tornado.escape import json_encode

from yowsup.layers import YowLayerEvent

class YowsupHandler(tornado.web.RequestHandler):
    def initialize(self, stack, messages):
        self.stack = stack
        self.messages = messages

class MainHandler(YowsupHandler):
    def get(self):
        self.stack.broadcastEvent(YowLayerEvent("sendMessage", dest='595981288424', msg='hello'))
        self.write("Hello, world")

class FetchMessagesHandler(YowsupHandler):
    def get(self):
        output = json_encode(self.messages)
        self.set_header( 'Content-Type', 'application/json' )
        self.write( output )

def make_app(stack, messages):
    return tornado.web.Application([
        (r"/messages", FetchMessagesHandler, dict(stack=stack, messages=messages)),
        (r"/", MainHandler, dict(stack=stack, messages=messages)),
    ])

# if __name__ == "__main__":
#     app = make_app()
#     app.listen(8888)
#    tornado.ioloop.IOLoop.current().start()
