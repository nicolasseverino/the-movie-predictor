#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Nicolas SEVERINO
"""

import mysql.connector
import sys
import argparse
import csv
import gzip
import re

from movie import Movie
from person import Person
from themoviedb import TheMovieDB
from omdb import OMDBApi
from genre import Genre

def connectToDatabase():
    return mysql.connector.connect(
        user='predictor',
        password='predictor',
        host='database',
        database='predictor'
    )

def clean(item):
    return item.strip()

def clean_duration(duration):
    if duration is not "Unknown":
        duration = re.findall(r"\d+", duration)[0]
        return int(duration)
    else:
        return duration

def clean_year(year):
    if year is not "Unknown":
        year = re.findall(r"\d+", year)[0]
        return int(year)
    else:
        return year

def disconnectDatabase(cnx):
    cnx.close()

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):    
    cursor.close()

def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {} LIMIT 1".format(table, id))

def findAllQuery(table):
    return ("SELECT * FROM {}".format(table))

def insert_people_query(person):
    insert_stmt = (
        "INSERT INTO `people` (`imdb_id`, `name`) "
        "VALUES (%s, %s)"
        "ON DUPLICATE KEY UPDATE `id`=`id`"
    )
    data = (person.imdb_id, person.name)
    return (insert_stmt, data)
    #return (f"INSERT INTO `people` (`firstname`, `lastname`) VALUES ('{person.firstname}', '{person.lastname}');")

def insert_movie_query(movie):
    insert_stmt = (
        "INSERT INTO `movies` (`imdb_id`, `original_title`, `duration`, `rating`, `release_date`, `synopsis`) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)"
        "ON DUPLICATE KEY UPDATE `id`=`id`"
    )
    data = (movie.imdb_id, movie.original_title, movie.duration, movie.rating, movie.release_date, movie.synopsis)
    return (insert_stmt, data)

def find(table, id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    query = findQuery(table, id)
    cursor.execute(query)
    results = cursor.fetchall()

    entity = None
    if (cursor.rowcount == 1):
        row = results[0]
        if (table == "movies"):
            entity = Movie(row['title'], row['original_title'], row['duration'], row['release_date'], row['rating'])

        if (table == "people"):
            entity = Person(
                row['firstname'],
                row['lastname']
            )
        
        entity.id = row['id']

    closeCursor(cursor)
    disconnectDatabase(cnx)

    return entity

def findAll(table):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findAllQuery(table))
    results = cursor.fetchall()  # liste de dictionnaires contenant des valeurs scalaires
    closeCursor(cursor)
    disconnectDatabase(cnx)
    if (table == "movies"):
        movies = []
        for result in results: # result: dictionnaire avec id, title, ...
            movie = Movie(
                title=result['title'],
                original_title=result['original_title'],
                duration=result['duration'],
                release_date=result['release_date'],
                rating=result['rating']
            )
            movie.id = result['id']
            movies.append(movie)
        return movies

    if (table == "people"):
        people = []
        for result in results: # result: dictionnaire avec id, title, ...
            person = Person(
                imdb_id=result['imdb_id'],
                name=result['name'],
            )
            person.id = result['id']
            people.append(person)
        return people

    if (table == "genres"):
        genres = []
        for result in results: # result: dictionnaire avec id, title, ...
            genre = Genre(name=result['name'])
            genre.id = result['id']
            genres[genre.name] = genre
        return genres

def insert_people(person):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(insert_people_query(person))
    cnx.commit()
    last_id = cursor.lastrowid
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return last_id

def insert_movie(movie):
    global cnx
    cursor = createCursor(cnx)
    (insert_stmt, data) = insert_movie_query(movie)
    cursor.execute(insert_stmt, params=data)
    cnx.commit()
    last_id = cursor.lastrowid
    closeCursor(cursor)
    return last_id

def insert_movies(movie):
    global cnx
    last_ids = []
    cursor = createCursor(cnx)
    i=0
    last_commit_i = 1
    for tconst,movie in movies.items():
        (insert_stmt, data) = insert_movie_query(movie)
        cursor.execute(insert_stmt, params=data)
        lastrowid = cursor.lastrowid
        if not lastrowid:
            movie = findMovieByImdbId(movie.imdb_id)
            lastrowid = movie.id
        last_ids.append(lastrowid)
        i = i+1
        if i % 1000 == 0:
            print(f"Committing {last_commit_i} to {i}")
            cnx.commit()
            last_commit_i = i
    print(f"Commiting {last_commit_i} to {len(movies)}")
    cnx.commit()
    closeCursor(cursor)
    return last_ids

def findMovieByImdbId(imdb_id):
    global cnx
    cursor = createCursor(cnx)
    cursor.execute("SELECT * FROM `movies` WHERE `imdb_id` = %s"), (imdb_id,))
    row = cursor.fetchone()
    closeCursor(cursor)
    movie = Movie()
    movie.id = row['id']
    movie.imbd_id = row['imbd_id']
    movie.original_title = row['original_title']
    return movie

def findPersonByImdbId(imdb_id):
    global cnx
    cursor = createCursor(cnx)
    cursor.execute("SELECT * FROM `people` WHERE `imdb_id` = %s"), (imdb_id,))
    row = cursor.fetchone()
    closeCursor(cursor)
    person = Person()
    person.id = row['id']
    person.imbd_id = row['imbd_id']
    person.name = row['name']
    return person

def insert_roles(roles):
    global cnx
    cursor = createCursor(cnx)
    for role in roles:
        insert_stmt = (
        "INSERT INTO `movies_people` (`movie_id`, `person_id`, `role`) "
        "VALUES (%s, %s, %s)"
        "ON DUPLICATE KEY UPDATE `role` = `role`"
        )
        data = (role['movie_id'], role['person_id'],role['role'])
        cursor.execute(insert_stmt,params=data)
    cnx.commit()
    closeCursor(cursor)

def printPerson(person):
    print("#{}: {} {}".format(person.id, person.firstname, person.lastname))

def printMovie(movie):
    print("#{}: {} released on {}".format(movie.id, movie.title, movie.release_date))

parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=('people', 'movies'), help='Le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitées du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exporté')

find_parser = action_subparser.add_parser('find', help='Trouve une entité selon un paramètre')
find_parser.add_argument('id' , help='Identifant à rechercher')

import_parser = action_subparser.add_parser('import', help='Importer un fichier CSV')
import_parser.add_argument('--file', help='Chemin vers le fichier à importer', required=False)
import_parser.add_argument('--api', help='Choix de l\'API à utiliser', required=False)
import_parser.add_argument('--imdb_id', help='ID Imdb à  importer depuis une API', required=False)

insert_parser = action_subparser.add_parser('insert', help='Insert une nouvelle entité')
known_args = parser.parse_known_args()[0]

if known_args.context == "people":
    insert_parser.add_argument('--firstname' , help='Prénom de la nouvelle personne', required=True)
    insert_parser.add_argument('--lastname' , help='Nom de la nouvelle personne', required=True)

if known_args.context == "movies":
    insert_parser.add_argument('--title' , help='Titre en France', required=True)
    insert_parser.add_argument('--duration' , help='Durée du film', type=int, required=True)
    insert_parser.add_argument('--original-title' , help='Titre original', required=True)
    insert_parser.add_argument('--release-date' , help='Date de sortie en France', required=True)
    insert_parser.add_argument('--rating' , help='Classification du film', choices=('TP', '-12', '-16'), required=True)

args = parser.parse_args()

cnx = connectToDatabase()

if args.context == "people":
    if args.action == "list":
        people = findAll("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].__dict__.keys())
                for person in people:
                    writer.writerow(person.__dict__.values())
        else:
            for person in people:
                printPerson(person)
    if args.action == "find":
        peopleId = args.id
        person = find("people", peopleId)
        printPerson(person)
    if args.action == "insert":
        print(f"Insertion d'une nouvelle personne: {args.firstname} {args.lastname}")
        person = Person(
            firstname=args.firstname,
            lastname=args.lastname
        )
        people_id = insert_people(person)
        print(f"Nouvelle personne insérée avec l'id '{people_id}'")

if args.context == "movies":
    if args.action == "list":  
        movies = findAll("movies")
        for movie in movies:
            printMovie(movie)
    if args.action == "find":  
        movieId = args.id
        movie = find("movies", movieId)
        if (movie == None):
            print(f"Aucun film avec l'id {movieId} n'a été trouvé ! Try Again!")
        else:
            printMovie(movie)
    if args.action == "insert":
        print(f"Insertion d'un nouveau film: {args.title}")
        movie = Movie(args.title, args.original_title, args.duration, args.release_date, args.rating)
        movie_id = insert_movie(movie)
        print(f"Nouveau film inséré avec l'id '{movie_id}'")
    if args.action == "import":
        if args.file:
            with open(args.file, 'r', encoding='utf-8', newline='\n') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    movie = Movie(
                        title=row['title'],
                        original_title=row['original_title'],
                        duration=row['duration'],
                        rating=row['rating'],
                        release_date=row['release_date']
                    )
                    movie_id = insert_movie(movie)
                    print(f"Nouveau film inséré avec l'id '{movie_id}'")
        if args.api != None:
            imdb_id = args.imdb_id
            if args.api == "themoviedb":
                the_movie_db = TheMovieDB()
                movie = the_movie_db.get_movie(imdb_id)
            if args.api == "omdb":
                omdb_api = OMDBApi()
                movie = omdb_api.get_movie(imdb_id)
            if (movie):
                movie_id = insert_movie(movie)
                print(f"'{movie.title}' importé depuis TheMovieDB ! Nouvel ID #{movie_id}")

if args.context =="dataset":
    if args.action == "import":
        with gzip.open("title.basics.tsv.gz","rt",encoding='utf-8') as tsvfile:
            rows = csv.DictReader(tsvfile,delimiter="\t", quoting=csv.QUOTE_NONE)
            movies=[]
            #i = 0
            for row in rows:
                # i = i+1
                # if i >=100:
                #     break
                if row['isAdult']=="1" or row['titleType'] !="movie":
                    #continue à la ligne suivante
                    continue
                print(row)
                #duration = row.get('runtimeMinutes', None #valeur si runtimeMinutes n'est pas présente)
                duration = row['runtimeMinutes']
                if duration == "\\N":
                    duration = None
                movie = Movie(
                    original_title = row['originalTitle'],
                    duration=duration,
                    release_date=None,
                    rating=None
                )
                movie.imdb_id = row['tconst']
                print(f"Ajout du film #{movie.imdb_id}")
                movies.append(movie)
            insert_movies(movie)
        with gzip.open("name.basics.tsv.gz","rt",encoding='utf-8') as tsvfile:
            rows = csv.DictReader(tsvfile,delimiter="\t", quoting=csv.QUOTE_NONE)
            people=[]
            for row in rows:
                print(row)
                person = Person(
                    imdb_id = row['nconst'],
                    name=row['name']
                )
                people.append(person)
            insert_people(people)
        with gzip.open("title.crew.tsv.gz","rt",encoding='utf-8') as tsvfile:
            rows = csv.DictReader(tsvfile,delimiter="\t", quoting=csv.QUOTE_NONE)
            for row in rows:
                print(row)
                tconst = row['tconst']
                directors_string = row['directors']
                writers_string = row['writers']
                #dans le documents tsv il y a des "\N" donc on échappe par un "\"
                directors = []
                writers = []
                if directors_string != "\\N":
                    directors = directors_string.split(',')
                if writers_string != "\\N":  
                    writers = writers_string.split(',')
                movie = findMovieByImdbId(tconst)
                movies_people = []
                for director_nconst in directors:
                    person = findPersonByImdbId(director_nconst)
                    movie_person={
                        'movie_id':movie.id,
                        'person_id':person.id,
                        'role':'director'
                    }
                    movies_people.append(movie_person)
                for writer_nconst in writers:
                    person = findPersonByImdbId(writer_nconst)
                    movie_person={
                        'movie_id':movie.id,
                        'person_id':person.id,
                        'role':'writer'
                    }
                insert_roles(movies_people)
disconnectDatabase(cnx)