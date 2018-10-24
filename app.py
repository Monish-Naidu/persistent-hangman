from flask import Flask
from api import api
from database import db

app = Flask(__name__)

api.init_app(app)

if __name__ == '__main__':
    app.run()  # starting a development server
