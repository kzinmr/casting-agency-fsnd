import os
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
import json
import datetime

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db


"""
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable
        to have multiple verisons of a database
"""


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    # these lines are added for unittests to pass
    actor = Actor(name="default", age=25, gender="male")
    actor.insert()
    movie = Movie(title="default", release_date=datetime.datetime.utcnow(),)
    movie.insert()


"""
Actor
a persistent actor entity, extends the base SQLAlchemy Model
"""


class Actor(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    name = Column(String(30))
    age = Column(Integer)  # positive int
    gender = Column(String(10))  # FIXME: Enum

    """
    insert()
        inserts a new model into a database
        the model must have a unique id or null id
        EXAMPLE
            actor = actor(name=req_name, age=req_age, gender=req_gender)
            actor.insert()
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = actor(name=req_name, age=req_age, gender=req_gender)
            actor.delete()
    """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            actor = actor.query.filter(actor.id == id).one_or_none()
            actor.name = 'Balack Obame'
            actor.update()
    """

    def update(self):
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
        }

    def __repr__(self):
        return json.dumps(self.to_dict())


"""
Movie
a persistent movie entity, extends the base SQLAlchemy Model
"""


class Movie(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    title = Column(String(80), unique=True)
    release_date = Column(DateTime)

    """
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.insert()
    """

    def insert(self):
        db.session.add(self)
        db.session.commit()

    """
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date)
            movie.delete()
    """

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'Black Coffee'
            movie.update()
    """

    def update(self):
        db.session.commit()

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "release_date": self.release_date.strftime("%m/%d/%y"),
        }

    def __repr__(self):
        return json.dumps(self.to_dict())
