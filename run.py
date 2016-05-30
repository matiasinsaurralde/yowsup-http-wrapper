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
from sys import argv
import tornado.ioloop, tornado.web

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

if len(argv) > 1:
    credentials = ( argv[1], argv[2])
    if len(argv) >= 4:
        port = argv[3]
    else:
        port = 8888
else:
    credentials = ( environ.get("PHONE"), environ.get("PASSWORD" ) )
    port = environ.get("PORT")

if __name__==  "__main__":

    messages = dict()

    stackBuilder = YowStackBuilder()
    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()

    stack.setProp("messages", messages)

    app = make_app(stack, messages)

    def YowThread():
        stack.setCredentials(credentials)
        stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
        stack.loop() #this is the program mainloop

    def TornadoThread():
        app.listen(port)
        tornado.ioloop.IOLoop.current().start()

    WaThread = threading.Thread( target=YowThread )
    WaThread.daemon = True
    WaThread.start()

    AppThread = threading.Thread( target=TornadoThread )
    AppThread.daemon = False
    AppThread.start()
