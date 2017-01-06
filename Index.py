#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: wushuiyong
# @Created Time : 日  1/ 1 23:43:12 2017
# @Description:

class Index(tornado.web.RequestHandler):
    def get(self):
        self.write('''
<html>
<head>
<script>
var ws = new WebSocket('ws://localhost:8000/soc');
ws.onmessage = function(event) {
    document.getElementById('message').innerHTML = event.data;
};
</script>
</head>
<body>
<p id='message'></p>
        ''')