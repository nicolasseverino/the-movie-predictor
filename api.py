import mysql.connector
import time
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

def connectToDatabase():
    return mysql.connector.connect(
        user='predictor',
        password='predictor',
        host='127.0.0.1',
        database='predictor'
    )

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

@app.route('/')
def index():
    return "<h1><center>Bienvenue ! Voici mon API pédagogique : TheMoviePredictor</center></h1><center><img src='https://external-preview.redd.it/g-P3AQqFtoMYggLbwnjpt4nUdNhJ47SESejQA6XIZX4.jpg?auto=webp&s=0ca5f9bd98a5746ab0d7311fadda5b5d7b2d1d82' style='max-width:50%'></center>"
    
@app.route('/movies', methods=['GET'])
def find_all_movies():
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute("SELECT * FROM movies")
    results = cursor.fetchall()
    movies = []
    for movie in results:
        movies.append(movie)
    return jsonify(movies)

@app.route('/movies/<int:id>', methods=['GET'])
def find_a_movie(id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute("SELECT * FROM movies WHERE id={}".format(id))
    results = cursor.fetchall()
    if (len(results) == 0):
            return "<h1><center>Aucun film ne correspond à cet ID</center></h1>"
    for aMovie in results:
        return jsonify(aMovie)


@app.route('/people', methods=['GET'])
def find_all_people():
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute("SELECT * FROM people")
    results = cursor.fetchall()
    people = []
    for aPerson in results:
        people.append(aPerson)
    return jsonify(people)

@app.route('/people/<int:id>', methods=['GET'])
def find_a_person(id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute("SELECT * FROM people WHERE id={}".format(id))
    results = cursor.fetchall()
    if (len(results) == 0):
            return "<h1><center>Personne ne correspond à cet ID</center></h1>"
    for aPerson in results:
        return jsonify(aPerson)


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)