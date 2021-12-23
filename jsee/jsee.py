#!/usr/bin/env python3

import typing
import logging
from inspect import signature, _empty
from flask import Flask, render_template, jsonify, request
from waitress import serve as wserve

def generate_schema (target, host='0.0.0.0', port=5050):
    hints = typing.get_type_hints(target, include_extras=False)
    target_args = target.__code__.co_varnames
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
        'url': f'http://{ host }:{ port }/run',
        'worker': False,
        'autorun': False
      },
      'inputs': inputs,
    }
    return schema


def serve(target, host='0.0.0.0', port=5050):
    schema = target if type(target) == dict else generate_schema(target, host, port)

    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    app = Flask(__name__)

    @app.route('/')
    def render():
        res = render_template('index.html', schema=schema, name=schema['model']['name'])
        return res

    @app.route('/run', methods=['POST'])
    def run():
        data = request.get_json(force=True)
        result = target(**data)
        return jsonify(result)

    wserve(app, host=host, port=port)
