# THE MOVIE PREDICTOR - POO

**BUT :** Scrapper les informations concernant un film grâce aux APIs TheMovieDB et OMDB et les insérer dans la base de données.  
La ligne de commande finale pour réaliser ces opérations doit être la suivante (ici tt7286456 est le film exemple) :
```bash
python app.py --api omdb --imdb_id tt7286456
```
ou
```bash
python app.py --api themoviedb --imdb_id tt7286456
```

## Démarrage du projet

Le projet comprend tout ce qu'il faut pour le faire tourner (l'application en elle-même ainsi que les accès à la base de données), à l'exception des clés API indispensables pour la récupération des données.

1. Créer un compte sur [TheMovieDB](https://www.themoviedb.org/?_dc=1573332904).

Une fois le compte créé et connecté, rendez-vous dans les paramètres (en haut à droite de la fenêtre) et cliquez sur "API" dans la sidebar à gauche. Remplissez tous les champs et vous recevrez une clé API par email.

2. Créer un compte sur [OMDB](https://www.omdbapi.com/apikey.aspx).

Renseignez votre adresse email et vous recevez votre clé API par email.

3. Créer un fichier **confidentiel** d'accès aux API : 
- Nommez le ".env" ;
- Structurez le ainsi :
> TMDB_API_KEY=*votre_clé_API_theMovieDB*  
> OMDB_API_KEY=*votre_clé_API_OMDB*

4. Enregistrez et sortez du fichier. Ouvrez votre terminal de commande et tapez :

```bash
docker-compose up
```
5. Une fois le container lancé, tapez l'une ou l'autre des lignes des commandes citées tout en haut.

## Auteur
**Nicolas SEVERINO** - [Autres projets](https://github.com/nicolasseverino/)