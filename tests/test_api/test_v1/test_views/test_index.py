#!/usr/bin/python3
from flask import Flask, render_template, abort, make_response, jsonify
from flask_cors import CORS
from models import storage
from os import getenv
from api.v1.views import app_views
from flasgger import Swaggerimport flaskr
import unittest
import json

class TestIndex(unittest.TestCase):
    '''
       Testing Index
    '''
    def setUpClass(self):
        self.app = app_views.test_client()
        self.app.testing = True

    def test_status(self):
        response = self.app('/status')
        data = json.loads(response.get_data())
        self.assertEqual(response.status_code, 200)
