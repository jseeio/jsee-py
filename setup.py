from setuptools import setup

setup(
  name='jsee',
  version='0.0.2',
  packages=['jsee'],
  scripts=['bin/jsee'],
  license='MIT',
  description='Simple GUI for processing tasks',
  author='Anton Zemlyansky',
  author_email='anton@zemlyansky.com',
  url='https://github.com/jseeio/jsee-py',
  install_requires=[
    'flask',
    'waitress',
  ],
)
