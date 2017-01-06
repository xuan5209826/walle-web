#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:
import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os


class Index(tornado.web.RequestHandler):
    def get(self):
        self.render('say.html')

# 然后再改改, 安排每个连接者给其它连接者打个招呼.

class SocketHandler(tornado.websocket.WebSocketHandler):


    clients = set()

    @staticmethod
    def send_to_all(message):
        for c in SocketHandler.clients:
            c.write_message(json.dumps(message))

    def open(self):
        self.write_message(json.dumps({
            'type': 'sys',
            'message': 'Welcome to WebSocket',
        }))
        SocketHandler.send_to_all({
            'type': 'sys',
            'message': str(id(self)) + ' has joined',
        })
        SocketHandler.clients.add(self)

    def on_close(self):
        SocketHandler.clients.remove(self)
        SocketHandler.send_to_all({
            'type': 'sys',
            'message': str(id(self)) + ' has left',
        })


    def on_message(self, message):
        out_file = '/tmp/ws_01'
        cmd = '%s > %s' % (message, out_file)
        done = os.system(cmd)
        stdOut = open(out_file)
        SocketHandler.send_to_all({
            'type': 'user',
            'id': id(self),
            'message': stdOut.read(),
        })
# class MainHandler(tornado.web.RequestHandler):
#     def get(self):
#         self.write("Hello, world")

def make_app():
    return tornado.web.Application([
        (r"/", Index),
        (r"/aso", SocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
