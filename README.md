# yowsup-http-wrapper

This project is a very simple HTTP wrapper for [Yowsup](https://github.com/tgalal/yowsup). It lets you fetch messages and send them. It uses Tornado.

## Implemented methods

I've been using [Postman](https://www.getpostman.com/) during my tests, you may find the methods and sample requests here:

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/84f6a0f6176ee409698b)

## Usage

I'm using this wrapper for a [proxy project](https://github.com/matiasinsaurralde/transports), which is written in Go. The Go program invokes the ```python``` interpreter with the right arguments and interacts with it through Tornado.

In case you're interested, the Go program runs something like this:

```python3 run.py 12341234 "whatsapp_password"```

Tornado will listen on **TCP port 8888** by default, if you plan to use an alternative port, you may append an additional argument:

```python3 run.py 12341234 "whatsapp_password" 8889```

It's important to note that this wrapper doesn't cover the Whatsapp registration process, so you'll have to do it by hand, using the ```yowsup-cli``` tool, check the [documentation](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0#yowsup-cli-registration). After you do a successful registration, you'll have a valid password to provide.

## Ideas

* Implement Whatsapp "presence", e.g. when Tornado is up, set presence as available.
* Implement [websockets](http://www.tornadoweb.org/en/stable/websocket.html#tornado-websocket-bidirectional-communication-to-the-browser)?
* Fix the [tests](https://github.com/matiasinsaurralde/yowsup-http-wrapper/blob/master/test_server.py), make them play well with Yowsup, handle two clients at the same time!

## License

[MIT](https://github.com/matiasinsaurralde/yowsup-http-wrapper/blob/master/LICENSE)
