from random import choice

import requests
from flask import Flask, request

load_balancer = Flask(__name__)

host = '127.0.0.1:5000'
servers = ['127.0.0.1:5001', '127.0.0.1:5002']
register = {host: servers}


@load_balancer.route('/', defaults={'path': ''})
@load_balancer.route('/<path:path>')
def router(path='/'):
    healthy_server = choice(register[host])

    if not healthy_server:
        return 'No backend servers available.', 503

    rewrite_path = path
    if path == '/':
        rewrite_path = ''
    response = requests.get(f'http://{healthy_server}/{rewrite_path}', headers=request.headers, params=request.args)
    return response.content, response.status_code
