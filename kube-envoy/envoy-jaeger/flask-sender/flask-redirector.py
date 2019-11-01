#!/usr/local/bin/python3

from flask import Flask, request, abort, jsonify, redirect

import socket
import os
import sys
import json
import requests
import time
import random

app = Flask(__name__)

@app.route('/')
def test():
    return redirect("http://myapp2:80")

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
