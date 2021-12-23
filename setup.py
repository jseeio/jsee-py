from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='jsee',
    version='0.0.2',
    packages=['jsee'],
    scripts=['bin/jsee'],
    license='MIT',
    description='Simple GUI for processing tasks',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Anton Zemlyansky',
    author_email='anton@zemlyansky.com',
    url='https://github.com/jseeio/jsee-py',
    install_requires=[
        'flask',
        'waitress',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
