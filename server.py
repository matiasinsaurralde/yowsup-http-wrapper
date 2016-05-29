import tornado.ioloop
import tornado.web
from tornado.escape import json_encode, json_decode

from yowsup.layers import YowLayerEvent

class YowsupHandler(tornado.web.RequestHandler):
    """Handler that references the Yowsup stack & the messages dictionary"""
    def initialize(self, stack, messages):
        self.stack = stack
        self.messages = messages

class MainHandler(YowsupHandler):
    def get(self):
        self.write("Hello, world")

class MessagesHandler(YowsupHandler):

    """Returns a JSON object with the incoming messages

    The client is expected to poll regularly.
    """
    def get(self):
        output = json_encode(self.messages)

        self.set_header( 'Content-Type', 'application/json' )
        self.write( output )

    """Sends a message to the specified number

    The input is a JSON Object, containing the destination number and the message body.
    """
    def post(self):
        input = json_decode( self.request.body)
        self.stack.broadcastEvent(YowLayerEvent( "sendMessage", dest=input['dest'], msg=input['msg']))

        self.set_header( 'Content-Type', 'application/json' )
        self.write( "true" )

    """Removes a message (if exists)
    """
    def delete(self):
        message_id = self.get_argument("id")
        if message_id in self.messages:
            del self.messages[message_id]

        self.write("true")

def make_app(stack, messages):
    return tornado.web.Application([
        (r"/messages", MessagesHandler, dict(stack=stack, messages=messages)),
        (r"/", MainHandler, dict(stack=stack, messages=messages)),
    ])
