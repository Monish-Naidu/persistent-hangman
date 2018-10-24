# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:abc123@localhost/postgres'
#db = SQLAlchemy(app)
db = SQLAlchemy(app)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    guesses = db.Column(db.String(80))
    word = db.Column(db.String(26))



db.create_all()
game1 = Game(id = 0, guesses = "w", word = "hello")
db.session.add(game1)
db.session.commit()
db.session.close()


    #game_id = db.Column(db.Integer, db.ForeignKey('game id'))


if __name__ == '__main__':
    app.run()  # starting a development server