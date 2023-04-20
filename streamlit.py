
import streamlit as st
from dotenv import load_dotenv
import os 
import pymongo
from pymongo.mongo_client import MongoClient



load_dotenv("/home/apprenant/Documents/01projet_python/DevIA_Roubaix/scrapy/test/series250/.env")

MONGODB_PWD = os.environ.get("MONGODB_PWD")
MONGODB_PSEUDO = os.environ.get("MONGODB_PSEUDO")


connection_todb = f"mongodb+srv://{MONGODB_PSEUDO}:{MONGODB_PWD}@cluster1.rdzhoip.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_todb)
db = client["imdb_data"]
collection = db["films_series"]


def recherche_par_titre(titre):
    resultats = collection.find({"titre": {"$regex": titre, "$options": "i"}})
    return list(resultats)


def recherche_par_acteur(acteurs):
    resultats = collection.find({"acteurs": {"$in": acteurs}})
    return resultats

def recherche_par_genre(genre):
    resultats = collection.find({"genre": {"$in": genre}})
    return resultats

def recherche_par_duree(max_duree):
    resultats = collection.find({"duree": {"$lte": max_duree}})
    return resultats

def recherche_par_note_min(note_min):
    resultats = collection.find({"score": {"$gte": note_min}})
    return resultats

st.title("Outils de recherche de films")
st.write("Entrez les critères de recherche ci-dessous")

st.title("Recherche de films par titre")
titre_recherche = st.text_input("Titre du film")
if titre_recherche:
    resultats = recherche_par_titre(titre_recherche)
    st.write(f"Nombre de résultats: {len(resultats)}")
    for film in resultats:
        st.write(film["titre"], "sorti en ", film["annee"], film["genre"], film["duree"],"Minutes")


acteurs = st.text_input("Recherche par acteur(s)")
if acteurs:
    acteurs = acteurs.split(",")
    resultats = recherche_par_acteur(acteurs)
    st.write("Résultats pour la recherche par acteur(s) :")
    for resultat in resultats:
        st.write(resultat["titre"])

genre = st.multiselect("Recherche par genre", options=['Romance','Drama','Musical','Sport','Family','Adventure','Comedy','Biography','Sci-Fi','Thriller','Horror','ActionWar','Animation','Film-Noir','Music','Fantasy','Western','Crime','Mystery','History'])
if genre:
    resultats = recherche_par_genre(genre)
    st.write("Résultats pour la recherche par genre :")
    for resultat in resultats:
        st.write(resultat["titre"])

max_duree = st.number_input("Recherche par durée (max)", min_value=0, max_value=300, step=5)
if max_duree:
    resultats = recherche_par_duree(max_duree)
    st.write("Résultats pour la recherche par durée :")
    for resultat in resultats:
        st.write(resultat["titre"])

note_min = st.number_input("Recherche par note minimale", value=0.0, min_value=0.0, max_value=10.0, step=0.1)
if note_min:
    resultats = recherche_par_note_min(note_min)
    st.write("Résultats pour la recherche par note minimale :")
    for resultat in resultats:
        st.write(resultat["titre"])