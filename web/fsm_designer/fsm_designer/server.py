# Copyright 2015 Cumulus Networks, Inc.

from gevent import monkey
monkey.patch_all()


import os
import socket
import pkg_resources
import logging
import hashlib
import yaml

from bottle import route, request
from bottle import static_file

from socketio.namespace import BaseNamespace
from socketio.mixins import BroadcastMixin

logger = logging.getLogger('fsm-designer.server')

saved_fsms_root = os.path.abspath("fsms")
print "saved_fsms_root %s" % saved_fsms_root

if not os.path.exists(saved_fsms_root):
    os.makedirs(saved_fsms_root)


class AgentNamespace(BaseNamespace, BroadcastMixin):

    def initialize(self):
        logger.debug("INIT")

    def on_save(self, message):
        logger.debug("save %s", message)
        data = yaml.safe_dump(message, default_flow_style=False)
        save_id = hashlib.sha1(data).hexdigest()
        url = '/save/{0}/fsm.yml'.format(save_id)
        with open(os.path.join(saved_fsms_root, save_id), 'w') as f:
            f.write(data)
        self.emit('saved', dict(url=url))


from socketio import socketio_manage


@route('/status')
def status():
    return "running"


@route('/socket.io/<remaining:path>')
def index(remaining):
    socketio_manage(request.environ, {'/fsm-designer': AgentNamespace})


@route('/save/<save_id:path>/fsm.yml')
def save(save_id):
    logger.debug("save_id %s", save_id)
    return static_file(save_id, root=saved_fsms_root, mimetype="text/yaml")


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
