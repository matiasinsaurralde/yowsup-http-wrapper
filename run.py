from yowsup.stacks import  YowStackBuilder
from layer import EchoLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.env                                import YowsupEnv

from os.path import join, dirname
from dotenv import load_dotenv

from os import environ

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

credentials = ( environ.get("PHONE"), environ.get("PASSWORD" ) )

if __name__==  "__main__":
    stackBuilder = YowStackBuilder()

    stack = stackBuilder\
        .pushDefaultLayers(True)\
        .push(EchoLayer)\
        .build()

    stack.setCredentials(credentials)
    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))   #sending the connect signal
    stack.loop() #this is the program mainloop
