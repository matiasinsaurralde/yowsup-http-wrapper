from tornado import testing, httpserver, gen
from tornado.httpclient import AsyncHTTPClient
from server import make_app, MessagesHandler

from tornado.escape import json_encode, json_decode

from time import sleep
from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env import YowsupEnv

'''
These tests are broken :(
$ python3 -m tornado.testing discover
'''

class TestMessages(testing.AsyncHTTPTestCase):
    '''Test MessagesHandler'''
    def get_app(self):
        messages = dict()
        stack = self.prepare_stack( (), messages)
        app = make_app(stack, messages)
        # stack.loop?
        return app

    def test_get_messages(self):
        response = self.fetch( '/messages' )
        body = response.body.decode('utf-8')
        assert response.headers['content-type'] == 'application/json'
        assert body == '{}'

    def test_send_message(self):
        message = {'dest': '12341234', 'msg': 'testmessage'}
        message_json = json_encode(message)
        response = self.fetch( '/messages', method='POST', body='{}', headers={'Content-Type': 'application/json'})

    def runTest(self):
        pass

    def prepare_stack(self, credentials, messages):
        stackBuilder = YowStackBuilder()
        stack = stackBuilder.pushDefaultLayers(True).push(EchoLayer).build()

        stack.setProp("messages", messages)
        stack.setCredentials(credentials)

        stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))

        return stack
