# THE MOVIE PREDICTOR - API

## Installation

Pour pouvoir utiliser ce script, il vous faut installer les packages suivant :
```bash
pip install mysql-connector-python
pip install flask
```
## Utilisation

Une fois le container lancé, ouvrez un terminal et tapez la commande suivante :
```bash
python app.py
```
ou 
```bash
flask run
```
Ouvrez un navigateur internet et rentrez l'url :
[127.0.0.1:5000]()

## Requêtes

Tapez à la fin de l'url : 
- GET :
    - [/movies]() : pour voir tous les films de la base de données ;
    - [/people]() : pour voir tous les acteurs de la base de données ;
    - [/movies/*id_a_taper*]() : pour voir les informations concernant le film dont on tape l'id ;
    - [/people/*id_a_taper*]() : pour voir l'acteur dont on tape l'id.
    
- ⚠ POST : *A venir*
- ⚠ DELETE : *A venir*