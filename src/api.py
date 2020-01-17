import datetime
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Actor, Movie
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
db = setup_db(app)
CORS(app)

"""
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
"""
db_drop_and_create_all()


# ROUTES
"""
    GET /actors
        it should be a public endpoint
        it should require the 'get:actors' permission
    returns status code 200 and json {"success": True, "actors": actors}
        where actors is the list of actors
        or appropriate status code indicating reason for failure
"""


@app.route("/actors")
@requires_auth("get:actors")
def get_actors(jwt):
    actors = Actor.query.all()
    print(actors)
    if len(actors) == 0:
        abort(404)
    else:
        actors = [actor.to_dict() for actor in actors]
        return jsonify({"success": True, "actors": actors})


"""
    POST /actors
        it should create a new row in the actors table
        it should require the 'post:actors' permission
    returns status code 200 and json {"success": True, "actors": actor}
        where actor an array containing only the newly created actor
        or appropriate status code indicating reason for failure
"""


@app.route("/actors", methods=["POST"])
@requires_auth("post:actors")
def create_actors(jwt):
    error = False
    try:
        data = request.json
        actor = Actor(name=data["name"], age=data["age"], gender=data["gender"])
        actor.insert()
        actors = [actor.to_dict()]
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        return jsonify({"success": True, "actors": actors})
    else:
        abort(422)


"""
    PATCH /actors/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:actors' permission
    returns status code 200 and json {"success": True, "actors": actor}
        where actor an array containing only the updated actor
        or appropriate status code indicating reason for failure
"""


@app.route("/actors/<int:actor_id>", methods=["PATCH"])
@requires_auth("patch:actors")
def edit_actors(jwt, actor_id):
    error = False
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
        abort(404)

    try:
        data = request.json
        if "name" in data:
            actor.name = data["name"]
        if "age" in data:
            actor.age = data["age"]
        if "gender" in data:
            actor.gender = data["gender"]
        actor.update()
        actors = [actor.to_dict()]
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        return jsonify({"success": True, "actors": actors})
    else:
        abort(422)


"""
    DELETE /actors/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:actors' permission
    returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@app.route("/actors/<int:actor_id>", methods=["DELETE"])
@requires_auth("delete:actors")
def delete_actors(jwt, actor_id):
    error = False
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

    if actor is None:
        abort(404)

    try:
        actor.delete()
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        return jsonify({"success": True, "delete": actor_id})
    else:
        abort(422)


"""
    GET /movies
        it should be a public endpoint
        it should require the 'get:movies' permission
    returns status code 200 and json {"success": True, "movies": movies}
        where movies is the list of movies
        or appropriate status code indicating reason for failure
"""


@app.route("/movies")
@requires_auth("get:movies")
def get_movies(jwt):
    movies = Movie.query.all()
    print(movies)
    if len(movies) == 0:
        abort(404)
    else:
        movies = [movie.to_dict() for movie in movies]
        return jsonify({"success": True, "movies": movies})


"""
    POST /movies
        it should create a new row in the movies table
        it should require the 'post:movies' permission
    returns status code 200 and json {"success": True, "movies": movie}
        where movie an array containing only the newly created movie
        or appropriate status code indicating reason for failure
"""


@app.route("/movies", methods=["POST"])
@requires_auth("post:movies")
def create_movies(jwt):
    error = False
    try:
        data = request.json
        if isinstance(
            data["release_date"], str
        ):  # NOTE: validate input format in the frontend
            data["release_date"] = datetime.datetime.strptime(
                data["release_date"], "%m/%d/%y"
            )
        movie = Movie(title=data["title"], release_date=data["release_date"])
        movie.insert()
        movies = [movie.to_dict()]
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        return jsonify({"success": True, "movies": movies})
    else:
        abort(422)


"""
    PATCH /movies/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:movies' permission
    returns status code 200 and json {"success": True, "movies": movie}
        where movie an array containing only the updated movie
        or appropriate status code indicating reason for failure
"""


@app.route("/movies/<int:movie_id>", methods=["PATCH"])
@requires_auth("patch:movies")
def edit_movies(jwt, movie_id):
    error = False
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)

    try:
        data = request.json
        if "title" in data:
            movie.title = data["title"]
        if "release_date" in data:
            if isinstance(data["release_date"], str):
                data["release_date"] = datetime.datetime.strptime(
                    data["release_date"], "%m/%d/%y"
                )
            movie.release_date = data["release_date"]
        movie.update()
        movies = [movie.to_dict()]
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        return jsonify({"success": True, "movies": movies})
    else:
        abort(422)


"""
    DELETE /movies/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:movies' permission
    returns status code 200 and json {"success": True, "delete": id}
        where id is the id of the deleted record
        or appropriate status code indicating reason for failure
"""


@app.route("/movies/<int:movie_id>", methods=["DELETE"])
@requires_auth("delete:movies")
def delete_movies(jwt, movie_id):
    error = False
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

    if movie is None:
        abort(404)

    try:
        movie.delete()
    except Exception:
        error = True
        db.session.rollback()
    finally:
        db.session.close()

    if not error:
        return jsonify({"success": True, "delete": movie_id})
    else:
        abort(422)


# Error Handling
"""
Example error handling for unprocessable entity
"""


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False, "error": 422, "message": "unprocessable"}), 422


@app.errorhandler(404)
def notfound(error):
    return (
        jsonify({"success": False, "error": 404, "message": "resource not found"}),
        404,
    )


@app.errorhandler(AuthError)
def autherror(error):
    return (
        jsonify(
            {
                "success": False,
                "error": error.status_code,
                "message": error.error["description"],
            }
        ),
        error.status_code,
    )
