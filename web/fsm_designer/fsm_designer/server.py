# Copyright 2015 Cumulus Networks, Inc.

from gevent import monkey
monkey.patch_all()

import gevent

import os
import time
import psutil
import getpass
import socket
import pkg_resources
import logging

from bottle import route, request
from bottle import static_file

import whisper


from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

logger = logging.getLogger('fsm-designer.server')


class AgentNamespace(BaseNamespace, BroadcastMixin):

    def initialize(self):
        logger.debug("INIT")

from socketio import socketio_manage

@route('/status')
def status():
    return "running"

@route('/socket.io/<remaining:path>')
def index(remaining):
    socketio_manage(request.environ, {'/fsm-designer': AgentNamespace})


@route('/<filename:path>')
def serve_static(filename):
    return static_file(filename, root=pkg_resources.resource_filename('fsm_designer', 'static'))


@route('/')
def root():
    return static_file('index.html', root=pkg_resources.resource_filename('fsm_designer', 'static'))


from bottle import ServerAdapter


class SocketIOServer(ServerAdapter):
    def run(self, handler):
        from socketio.server import SocketIOServer
        resource = self.options.get('resource', 'socket.io')
        policy_server = self.options.get('policy_server', False)
        done = False
        while not done:
            try:
                SocketIOServer((self.host, self.port),
                               handler,
                               resource=resource,
                               policy_server=policy_server,
                               transports=['xhr-multipart', 'xhr-polling']).serve_forever()
            except socket.error, e:
                if e.errno == 98:
                    logger.warning(str(e))
                    raise
                else:
                    raise
