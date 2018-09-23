from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

import sys
import argparse
import random

from solver.solver import solver
from flask import Flask, request, jsonify
import json
from prometheus_client import Counter, start_wsgi_server as prometheus_server



MAX_VALUE = 1000

app = Flask(__name__)
app.config.from_object(__name__)
requests_total = Counter('requests_total', 'Total number of requests')


# The root endpoint returns the app value. Some percentage of the time
# (given by app.config['failure_rate']) calls to this endpoint will cause the
# app to crash (exits non-zero).
@app.route('/v1/')
def index():
    input_val = json.loads(request.args.get("input"))
    colors=input_val.get("colors")
    customers=input_val.get("customers")
    demands=input_val.get("demands")
    solution = solver(colors, customers, demands)
    if solution:
      return " ".join(map(str, solution))
    else:
      return "IMPOSSIBLE"

@app.route('/v2/', methods=['GET', 'POST'])
def index_v2():
    colors = int(request.values.get("colors"))
    customers = int(request.values.get("customers"))
    demands = json.loads(request.values.get("demands"))
    solution = solver(colors, customers, demands)
    if solution:
      return jsonify({ 'solution': solution })
    else:
      return jsonify({ 'code': 'IMPOSSIBLE', 'message': 'Impossible to find a solution' })

# To help with testing this endpoint will cause the app to crash
# every time it is called
@app.route('/crash')
def crash():
    requests_total.inc()
    request.environ.get('werkzeug.server.shutdown')()
    app.config.update({'crashed': True})
    return "{}"


def main(args):
    prometheus_server(args.monitor)

    app.config.update({
        'input': args.input,
        'failure_rate': args.failure_rate,
        'crashed': False
    })
    app.run('0.0.0.0', port=args.port)

    if app.config['crashed']:
        print('app crashed, exiting non-zero')
        sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input',
        type=str,
        required=False,
        help='the input string'
    )
    parser.add_argument(
        '--port',
        type=int,
        required=True,
        help='the serving port'
    )
    parser.add_argument(
        '--monitor',
        type=int,
        required=True,
        help='the monitoring port'
    )
    parser.add_argument(
        '--failure-rate',
        type=float,
        default=0.2,
        help='the failure rate'
    )
    return parser.parse_args()


if __name__ == '__main__':
    main(parse_args())
