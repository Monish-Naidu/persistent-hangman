from flask_restplus import Api
from .Game import api as game_api


api = Api(title='HangMan API', version='1.0', description='A super rad hang man api')

api.add_namespace(game_api)

