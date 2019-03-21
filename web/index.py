#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bottle import Bottle, run, error, static_file
from removehistory import get_history
import json


def web_run(host="127.0.0.1", port=17891):
    app = Bottle()

    @error(404)
    def error404(err):
        return 'Nothing here, sorry' + err

    @app.route('/')
    def index():
        return static_file('index.html', root='web/templates')

    @app.route('/data')
    def index():
        return json.dumps(get_history())

    run(app, host=host, port=port)


if __name__ == '__main__':
    web_run()
