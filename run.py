from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env                                import YowsupEnv

from os.path import join, dirname
from dotenv import load_dotenv
from os import environ

from server import make_app

import threading, time
import tornado.ioloop, tornado.web

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

credentials = ( environ.get("PHONE"), environ.get("PASSWORD" ) )

if __name__==  "__main__":

    stackBuilder = YowStackBuilder()
    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()

    app = make_app(stack)

    def YowThread():
        stack.setCredentials(credentials)
        stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
        stack.loop() #this is the program mainloop

    def TornadoThread():
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()

    WaThread = threading.Thread( target=YowThread )
    WaThread.daemon = True
    WaThread.start()

    AppThread = threading.Thread( target=TornadoThread )
    AppThread.daemon = False
    AppThread.start()
