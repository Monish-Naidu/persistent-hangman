from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, marshal, fields
import random
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from flask_cors import CORS, cross_origin



app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, title='HangMan Game', version='1.0', description='An awesome hangman API')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc123@localhost/postgres'
CORS(app)
ns = api.namespace('Game', description='An amazing hangman API')

db = SQLAlchemy(app)

game = api.model('Game', {
      'word': fields.String(description='The word to guess'),
      'known': fields.String(description='known letters'),
      'guessed': fields.String(description='guessed letters')
})

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
    known = db.Column(db.String(200))
    guessed = db.Column(db.String(50))





db.create_all()

HangmanWords = ["monish", "brian", "jimmy", "john", "robert", "goat"]

curr_state = {
    "message": "",
    "known": [],
    "guessed": []
}

def create_game():
    new_word = random.choice(HangmanWords)
    known_letters = ""
    for i in range(len(new_word)):
        known_letters += "*"
    guessed_letters = ""
    new_game = Game(word=new_word, known= known_letters, guessed=guessed_letters)
    db.session.add(new_game)
    db.session.commit()
    #db.session.close()
    return new_game






def find_game(game_id):
    game = Game.query.filter(Game.id == game_id).one()
    return game



def letter_guess(game_id, guess):
    game = Game.query.filter(Game.id == game_id).one()
    curr_state = {"message": "This is how the game is currently!", "known": game.known, "guessed": game.guessed}
    if len(guess) != 1:
        curr_state["message"] = "The guess was not one letter"
        return jsonify(game.id, game.guessed, game.known)
    if guess not in "abcdefghijklmnopqrstuvwxyz":
        curr_state["message"] = "The letter " + guess + " is not part of the alphabet"
        return jsonify(game.id, game.guessed, game.known)
    if guess in game.known:
        curr_state["message"] = "You have already guessed " + guess + " try again"
        return jsonify(game.id, game.guessed, game.known)
    if guess in game.word:
        charArr = list(game.known)
        arrGuessed = list(game.guessed)
        wordArr = list(game.word)
        for i in range(0, len(game.word)):
            if guess == wordArr[i]:
                charArr[i] = guess
                game.known = ''.join(charArr)
                #game.known = game.known[0:i-1] + guess + game.known[i+1:]
        curr_state["known"] = list(game.known)
        arrGuessed.append(guess)
        game.guessed = "".join(arrGuessed)
        curr_state["guessed"] =game.guessed
        curr_state["message"] = "Good job playa! the letter " + guess + " is in the word!"
        db.session.commit()
        return jsonify(game.id, game.guessed, game.known)
    if guess not in game.word:
        list_guessed =list(game.guessed)
        list_guessed.append(guess)
        curr_state["guessed"] = "".join(list_guessed)
        curr_state["message"] = guess + " is not in the word"
        game.guessed = curr_state["guessed"]
        db.session.add(game)
        db.session.commit()
        return jsonify(game.id, game.guessed, game.known)

def delete_game(game_id):
    game = Game.query.filter(Game.id == game_id).one()
    db.session.delete(game)
    db.session.commit()


curr_state = {
    "message": "",
    "known": [],
    "guessed": []
}
game_state = {
    "id": 0
}

@ns.route('/', methods=['POST'])
@ns.response(404, 'unsuccessful request')
@ns.response(200, 'successful request')
class game_operations(Resource):

    def post(self):
        '''
        Creates a new hangman game and returns id of the game.
        '''
        new_game = create_game()
        return jsonify(new_game.id)



@ns.route('/<int:game_id>', methods=['PUT', 'DELETE', 'GET'])
@ns.response(404, 'unsuccessful request')
@ns.response(200, 'successful request')
class GameStatus(Resource):
#TODO: find out why  Object of type Game is not JSON serializable from get method

    def get(self, game_id):
        '''
        Finds a current game from given id.
        '''
        my_game = Game.query.filter_by(id=game_id).first()
        #TODO: replace with get_game function
        if my_game is None:
            return "Invalid game ID"

        curr_state = {
            "message": "This is how the game is currently!",
            "known": my_game.known,
            "guessed": my_game.guessed
        }
        return jsonify(curr_state)




    def delete(self, game_id):
        '''
        Deletes a game from a given id.
        '''
        delete_game(game_id)
        return "Game deleted successfully", 200


@ns.route('/<int:game_id>/<string:guess>', methods=['PUT'])
@ns.response(404, 'unsuccessful request')
@ns.response(200, 'successful request')
class GameStatus(Resource):
    def put(self, game_id, guess):
        '''
        Updates the hangman game with the letter guessed.
        '''
        return letter_guess(game_id, guess)









if __name__ == '__main__':
    app.run