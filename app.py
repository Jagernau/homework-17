# app.py

from flask import Flask, jsonify, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from schemas import movie_schema, movies_schema
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False}


db = SQLAlchemy(app)
api = Api(app)
movie_ns = api.namespace('movies')


@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):
        all_movies = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating, Movie.trailer, Genre.name.label('genre'), Director.name.label('director')).join(Genre).join(Director).all()
        return movies_schema.dump(all_movies), 200

    def post(self):
        req_json = request.json
        new_movie = Movie(**req_json)
        with db.session.begin():
            db.session.add(new_movie)
        return f"Новый объект с id {new_movie.id} создан!", 201


@movie_ns.route("/<int:movie_id>")
class MovieView(Resource):
    def get(self, movie_id: int):       
        movie = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating, Movie.trailer, Genre.name.label('genre'), Director.name.label('director')).join(Genre).join(Director).filter(Movie.id==movie_id).first()
        if movie:
            return movie_schema.dump(movie),200
        return "Нет такого фильма", 404

    def patch(self, movie_id: int):
        movie = db.session.query(Movie.id, Movie.title, Movie.description, Movie.rating, Movie.trailer, Genre.name.label('genre'), Director.name.label('director')).join(Genre).join(Director).filter(Movie.id==movie_id).first()
        if not movie:
            return "Нет такого фильма", 404

        req_json = request.json
        if 'title' in req_json:
            movie.title = req_json['title']
        elif 'description' in req_json:
            movie.title = req_json['description']
        elif 'trailer' in req_json:
            movie.title = req_json['trailer']
        elif 'year' in req_json:
            movie.title = req_json['year']
        elif 'rating' in req_json:
            movie.title = req_json['rating']
        elif 'genre_id' in req_json:
            movie.title = req_json['genre_id']
        elif 'director_id' in req_json:
            movie.title = req_json['director_id']
        db.session.add(movie)
        db.session.commit()
        return f"Объект с id {movie.id} обновлён!", 204











if __name__ == '__main__':
    app.run(debug=True)
