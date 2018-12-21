from flask import Flask, request, jsonify
from flask_restplus import Api, Resource, marshal, fields
from random import randint
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, title='HangMan Game', version='2.0', description='8 Letter Hangman')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://qhorbnemvvdrvx:924c0c30b234467274e53557a246c66e5cd79079e3a24abcb0d49e5adc765d01@ec2-107-22-189-136.compute-1.amazonaws.com:5432/d9eo3h2pqak26b'
ns = api.namespace('Hangman', description='We are going to play hangman. '
                                          'Please only guess lowercase letters. You only have 6 guesses')
parser = api.parser()
hangman_database = SQLAlchemy(app)

class single_game(hangman_database.Model):
    id = hangman_database.Column(hangman_database.Integer, primary_key=True)
    tries_left = hangman_database.Column(hangman_database.Integer)
    magic_word = hangman_database.Column(hangman_database.String)
    known_letters = hangman_database.Column(hangman_database.String)
    guessed_letters = hangman_database.Column(hangman_database.String)


hangman_database.create_all()

@ns.route('/game')
@app.route('/game', methods=['GET', 'POST'])
class make_game(Resource):

    BagOfWords = ["zigzaggy", "skipjack", "aardvark", "butthead", "testings", "zabajone", "jezebels", "cybersex"]
    MagicWord = BagOfWords[randint(0, 7)]
    known = "********"
    tries = 6
    word_bank = ""

    @ns.doc("Creates a new game and returns the game ID")
    def post(self):
        i = 0
        while hangman_database.session.query(single_game.id).filter_by(id=i).scalar() is not None:
            i = i + 1
        game_to_be_added = single_game(id = i,
                                       magic_word = self.MagicWord,
                                       known_letters = self.known,
                                       tries_left = self.tries,
                                       guessed_letters = self.word_bank)
        game_to_be_added.id = i
        game_to_be_added.magic_word = self.MagicWord
        game_to_be_added.known_letters = self.known
        game_to_be_added.tries_left = self.tries
        game_to_be_added.guessed_letters = self.word_bank
        hangman_database.session.add(game_to_be_added)
        hangman_database.session.commit()
        hangman_database.session.close()
        return "this is the game ID " + str(i), 200

    @ns.param('id', 'the game id')
    @ns.doc("Retrieves the current state of this game")
    def get(self):
        curr_id = request.args.get('id')
        #curr_game = hangman_database.query.filter_by(id=curr_id).first()
        #curr_game = hangman_database.session.filter_by(id=curr_id).first()
        #curr_game = hangman_database.session.query_property(single_game.id).filter_by(id=curr_id)
        #curr_game = hangman_database.session.query(single_game.id).filter_by(id=curr_id)
        #curr_game = single_game.query.get(id=curr_id)
        curr_game = single_game.query.filter_by(id = curr_id).first()
        #curr_game = hangman_database.filter_by(id=curr_id).first()

        #return jsonify(curr_game)

        if curr_game is None:
            return "Invalid game ID"

        curr_state = {
            "message": "this is the current state of the game",
            "known": curr_game.known_letters,
            "tries": curr_game.tries_left,
            "guessed": curr_game.guessed_letters
        }
        return jsonify(curr_state)

    @ns.param('id', 'the game id')
    @ns.doc("Retrieves the current state of this game")
    def delete(self):
        curr_id = request.args.get('id')
        curr_game = single_game.query.filter_by(id=curr_id).first()
        if curr_game is None:
            return "Invalid game ID"

        hangman_database.session.delete(curr_game)
        hangman_database.session.commit()
        hangman_database.session.close()
        return "Game " + str(id) + " has been deleted!"


@ns.route('/guess')
@app.route('/guess', methods=['GET', 'POST'])
class play_game(Resource):
    BagOfWords = ["zigzaggy", "skipjack", "aardvark", "butthead", "testings", "zabajone", "jezebels", "cybersex"]
    MagicWord = BagOfWords[randint(0, 7)]
    known = "********"
    tries = 6
    word_bank = ""






    @ns.doc("Guess a single lower case letter")
    @ns.param('letter', 'the letter you are guessing')
    @ns.param('id', 'The game id')
    @app.route('/put/<string:letter>')
    def put(self):
        letter = request.args.get('letter')
        curr_id = request.args.get('id')
        """Retrieves the game from the database and ensures it is valid"""
        curr_game = single_game.query.filter_by(id=curr_id).first()
        if curr_game is None:
            return "Invalid game ID"
        self.MagicWord = curr_game.magic_word
        self.known = curr_game.known_letters
        self.tries = curr_game.tries_left
        self.word_bank = curr_game.guessed_letters


        curr_state = {
            "message": "",
            "known": self.known,
            "tries": self.tries,
            "guessed": self.word_bank
        }








        if "*" not in self.known:
            return "YOU WIN"

        if (self.tries == 0):
            return "YOU LOSE"

        if (len(letter) != 1):
            curr_state["message"] = "you can only guess 1 letter at a time"
            return jsonify(curr_state)
        if letter in self.word_bank:
            curr_state["message"] = "You have already guessed that letter!"
            return jsonify(curr_state)
        if letter not in "abcdefghijklmnopqrstuvwxyz":
            curr_state["message"] = "Must be a lower case letter!"
            return jsonify(curr_state)

        if letter not in self.MagicWord:
            self.tries = self.tries - 1
            curr_state["tries"] = self.tries
            list_word_bank = list(self.word_bank)
            list_word_bank.append(letter)
            self.word_bank = "".join(list_word_bank)
            curr_state["message"] = "The letter " + letter + " is not it our word"

            """Updates the record and inserts it back into the database"""
            curr_game.magic_word = self.MagicWord
            curr_game.known_letters = self.known
            curr_game.tries_left = self.tries
            curr_game.guessed_letters = self.word_bank
            hangman_database.session.commit()
            hangman_database.session.close()
            curr_state["guessed"] = self.word_bank
            curr_state["known"] = self.known
            return jsonify(curr_state)

        charArray = list(self.known)
        for i in range(0,len(self.MagicWord)):
            if letter == self.MagicWord[i]:
                charArray[i] = self.MagicWord[i]
        self.known = "".join(charArray)

        list_word_bank = list(self.word_bank)
        list_word_bank.append(letter)
        self.word_bank = "".join(list_word_bank)

        curr_state["message"] = "The letter " + letter + " is in our word!"
        curr_state["known"] = self.known
        curr_state["tries"] = self.tries
        curr_state["guessed"] = self.word_bank

        """Updates the record and inserts it back into the database"""
        curr_game.magic_word = self.MagicWord
        curr_game.known_letters = self.known
        curr_game.tries_left = self.tries
        curr_game.guessed_letters = self.word_bank
        hangman_database.session.commit()
        hangman_database.session.close()

        return jsonify(curr_state)



if __name__ == '__main__':
    app.run(debug=True)