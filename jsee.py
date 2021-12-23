import argparse
import importlib
import typing

import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

from inspect import signature, _empty
from flask import Flask, render_template, jsonify, request
from waitress import serve

parser = argparse.ArgumentParser()
parser.add_argument('module_name')
parser.add_argument('target_name')
parser.add_argument('--port', dest='port', default=5050)
parser.add_argument('--host', dest='host', default='0.0.0.0')

args = parser.parse_args()

module = importlib.import_module(args.module_name.split('.')[0])
target = getattr(module, args.target_name)

hints = typing.get_type_hints(target, include_extras=False)
target_args = target.__code__.co_varnames

app = Flask(__name__)

inputs = []
for a in target_args:
    t = 'string'
    if a in hints:
        hint = hints[a]
        if hint == int:
            t = 'int'
        elif hint == float:
            t = 'float'
        elif hint == bool:
            t = 'checkbox'
    input_object = {
        'name': a,
        'type': t
    }
    default_value = signature(target).parameters[a].default
    if default_value is not _empty:
      input_object['default'] = default_value
    inputs.append(input_object)


schema = {
  'model': {
    'type': 'post',
    'url': f'http://{ args.host }:{ args.port }/run',
    'worker': False,
    'autorun': False
  },
  'inputs': inputs,
}

@app.route('/')
def render():
    res = render_template('index.html', schema=schema, module_name=args.module_name, target_name=args.target_name)
    return res

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json(force=True)
    result = target(**data)
    return jsonify(result)

serve(app, host=args.host, port=args.port)
