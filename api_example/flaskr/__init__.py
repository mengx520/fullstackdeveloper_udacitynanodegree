from flask import Flask, jsonify
from models import db, Plant
from flask_cors import CORS, cross_origin

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTION')
        return response
    
    #@cross_origin
    @app.route('/')
    def hello_world():
        return jsonify({'message':'HELLO, WORLD!'})
    return app



