#!/usr/bin/env python3

import typing
import logging
from inspect import signature, _empty
from flask import Flask, render_template_string, jsonify, request
from waitress import serve as wserve

template = """
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <title>{{ name }}</title>
    <style>
      body {
        font-family: sans-serif;
      }

      h1 {
        font-weight: 300;
        font-size: 22px;
      }

      .container {
        max-width: 1100px;
        margin: auto;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>{{ name }}</h1>
      <div id="jsee-container"></div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/@jseeio/jsee@{{ version }}/dist/jsee.js"></script>
    <!-- <script src="http://localhost:8080/dist/jsee.js"></script> -->
    <script>
      const schema = JSON.parse('{{schema | tojson}}')
      const env = new JSEE({
        container: document.getElementById('jsee-container'),
        schema: schema
      })
    </script>
</body>
</html>
"""

def generate_schema (target, host='0.0.0.0', port=5050):
    hints = typing.get_type_hints(target)
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
        'name': target.__name__,
        'type': 'post',
        'url': f'http://{ host }:{ port }/run',
        'worker': False,
        'autorun': False
      },
      'inputs': inputs,
    }
    return schema


def serve(target, host='0.0.0.0', port=5050, version='0.2'):
    schema = target if type(target) == dict else generate_schema(target, host, port)

    logger = logging.getLogger('waitress')
    logger.setLevel(logging.INFO)

    app = Flask(__name__)

    @app.route('/')
    def render():
        res = render_template_string(
            template,
            schema=schema,
            name=schema['model']['name'],
            version=version
        )
        return res

    @app.route('/run', methods=['POST'])
    def run():
        data = request.get_json(force=True)
        result = target(**data)
        return jsonify(result)

    wserve(app, host=host, port=port)
