# JSEE interface for native Python functions

JSEE.py uses typing hints to infer a target function schema and generate a new Flask server and corresponding GUI. Very experimental

Usage:
```
jsee FILE_NAME FUNCTION_NAME [--port PORT] [--host HOST]
```
for example:
```
jsee example.py sum
```
