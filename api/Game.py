from flask_restplus import Resource, Namespace, fields, reqparse


api = Namespace('Games', description='Operations related to a hangman api')

game_model = api.model('Game', {
    'id': fields.Integer(readOnly=True, description='The unique ID of the game'),
    'guesses': fields.Integer(readOnly=True, description= 'The guesses already made'),
    'word': fields.String(required=True, description = 'The word to be guessed')

})



#parser = reqparse.RequestParser()
#parser.add_argument('id', required=False)
#parser.add_argument('Name', required=False)

class Game:
    def __init__(self, id, guesses, word):
        self.id = id
        self.guesses = guesses
        self.word = word


games = []

@api.response(202, 'Accepted')
@api.response(404, 'Could not find any game')
@api.route('/')
class GameCollection(Resource):
    # TO-DO: add marshalling to get only specific fields
    def get(self):
        '''
            Return a list of games
            '''
        #TODO add get logic

        # TO-DO: create querying for list of users using db
        return games

    @api.response(404, 'Could not create a new game')
    #@api.expect(user_model, validate=True) TODO: Generate our own game with a new word, game ID, and empty guesses
    def post(self):
        """

            Creates a new game.

            """
        TODO: return the id of the agme 
        return None


@api.response(404, 'Could not get that specific game')
@api.route('/game/<int:id>')
@api.doc(params={'id': 'An ID for a game'})
class GameOperations(Resource):
    def get(self, id):
        """

            Returns a specific game.

            """
        #TODO: add get method, using query from db
        return games[id],

    @api.response(404, 'Could not update current user')
    def put(self, id):
        '''

        Updates a current game

        '''
        return None


    @api.response(202, 'Game successfully deleted.')
    @api.response(404, 'Game could not be deleted')
    def delete(self, id):
        """

            Deletes a game
            .

            """
        #TODO: create delete_user method
        return None
