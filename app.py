from flask import Flask, jsonify, request
from flask_restplus import Api, Resource, reqparse
import random
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, title='HangMan Game', version='1.0', description='An awesome hangman API')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc123@localhost/postgres'

ns = api.namespace('Game', description='An amazing hangman API')

db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String)
    known = db.Column(db.String(200))
    guessed = db.Column(db.String(50))





db.create_all()

HangmanWords = ["monish", "brian", "jimmy", "john", "robert", "goat"]

word_database = {
    "guessed": [],
    "known": [],
    "message": ""
}

def create_game():
    new_word = random.choice(HangmanWords)
    known_letters = []
    for i in range(len(new_word)):
        known_letters.append("_")
    guessed_letters = []
    new_game = Game(word=new_word, known= known_letters, guessed= guessed_letters)
    db.session.add(new_game)
    db.session.commit()
    #db.session.close()
    return new_game






def find_game(game_id):
    game = Game.query.filter(Game.id == game_id).one()
    return game


def guess_letter(game_id, guess):
    game = Game.query.filter(Game.id == game_id).one()
    word_database["guessed"] = game.guessed_letters
    word_database["known"] = game.known_letters
    if len(guess) != 1:
        word_database["message"] = "The guess was not one letter"
        return jsonify(word_database)
    if guess not in "abcdefghijklmnopqrstuvwxyz":
        word_database["message"] = "The letter " + guess + " is not part of the alphabet"
        return jsonify(word_database)
    if guess in word_database["guessed"]:
        word_database["message"] = "You have already guessed " + guess + " try again"
        return jsonify(word_database)
    if guess in game.word:
        for i in range(0, len(game.word)):
            if guess == game.word[i]:
                word_database["known"][i] = guess
                game.known_letters = word_database["known"]
        word_database["guessed"].append(guess)
        game.guessed_letters = word_database["guessed"]
        word_database["message"] = "Good job playa! the letter " + guess + " is in the word!"
        db.session.add(game)
        db.session.commit()
        return jsonify(word_database)
    if guess not in game.word:
        word_database["message"] = guess + " is not in the word"
        word_database["guessed"].append(guess)
        return jsonify(word_database)



def delete_game(game_id):
    game = Game.query.filter(Game.id == game_id).one()
    db.session.delete(game)
    db.session.commit()

parser = reqparse.RequestParser()
parser.add_argument('id', required=True)
parser.add_argument('guess', required=True)

@ns.route('/')
class game_operations(Resource):

    def post(self):
        '''
        Creates a new hangman game and returns id of the game.
        '''
        new_game = create_game()
        return "The game id is:  " + str(new_game.id), 200

@ns.route('/<int:id>')
@ns.response(401, 'requests that are not successful, please pick the available game id')
@ns.response(200, 'requests that are successful (i.e a game_id that is good)')
@ns.response(500, 'requests that are not successful, (i.e a game_id that is not valid)')
class GameStatus(Resource):
#TODO: find out why  Object of type Game is not JSON serializable from get method

    def get(self, id):
        '''
        Finds a current game from given id.
        '''
        game = find_game(id)
        word_database["guessed"] = game.guessed
        word_database["known"] = game.known
        return jsonify(word_database), 200

    def delete(self, id):
        '''
        Deletes a game from a given id.
        '''
        delete_game(id)
        return "Game deleted successfully", 200


    def put(self):
        '''
        Updates the hangman game with the letter guessed.
        '''
        guess = request.args.get('letter')
        id = request.args.get('id')
        guess_letter(id, guess)

        return "Guess successful", 200







if __name__ == '__main__':
    app.run(debug=True)