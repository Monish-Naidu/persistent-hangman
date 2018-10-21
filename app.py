from flask import Flask, request, jsonify
from flask_restplus import Api

api = Api(title='Hangman API', version='1.0', description='The first iteration of my hangman API')

app = Flask(__name__)

#api.init_app(api) TODO: currently causes an error

word = "vivek"


word_database = {
    "guessed": [],
    "known": ["", "", "", "", ""],
    "message": ""
}

@app.route('/game')
def new_game():
    return 'Creating a new game, good luck!'


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/start')
def start():
    return "starting a hangman game"

@app.route('/guess')
def guess():
    guess = request.args.get('letter')
    if len(guess) != 1:
        word_database["message"] = "The guess was not one letter"
        return jsonify(word_database)
    if guess not in "abcdefghijklmnopqrstuvwxyz":
        word_database["message"] = "The letter " + guess + " is not part of the alphabet"
        return jsonify(word_database)
    if guess in word_database["guessed"]:
        word_database["message"] = "You have already guessed " + guess + " try again"
    if guess in word:
        for i in range(0, len(word)):
            if guess == word[i]:
                word_database["known"][i] = guess
        word_database["guessed"].append(guess)
        word_database["message"] = "Good job playa! the letter " + guess + " is in the word!"
        return jsonify(word_database)
    if guess not in word:
        word_database["message"] = guess + " is not in the word"
        word_database["guessed"].append(guess)
        return jsonify(word_database)




if __name__ == '__main__':
    app.run(debug=True)  # starting a development server
