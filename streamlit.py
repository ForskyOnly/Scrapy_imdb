
import streamlit as st
from dotenv import load_dotenv
import os 
import pymongo
from pymongo.mongo_client import MongoClient



load_dotenv("/home/apprenant/Documents/01projet_python/DevIA_Roubaix/scrapy/test/series250/.env")

MONGODB_PWD = os.environ.get("MONGODB_PWD")
MANGODB_PSEUDO = os.environ.get("MANGODB_PSEUDO")


connection_todb = f"mongodb+srv://{MANGODB_PSEUDO}:{MONGODB_PWD}@cluster1.rdzhoip.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_todb)
db = client["imdb_data"]
collection = db["films_series"]


def recherche_par_nom(nom):
    resultats = collection.find({"$text": {"$search": nom}})
    return resultats

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

st.title("Recherchez un film")
st.write("Entrez les critères de recherche ci-dessous")

nom = st.text_input("Recherche par nom")
if nom:
    resultats = recherche_par_nom(nom)
    st.write("Résultats pour la recherche par nom :")
    for resultat in resultats:
        st.write(resultat["titre"])

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