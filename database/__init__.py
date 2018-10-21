from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def reset_database():
   #TODO import models
    db.drop_all()
