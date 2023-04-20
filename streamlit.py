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


st.sidebar.subheader("Filtre de recherche par catégorie")
categorie = st.sidebar.selectbox("Catégorie", ["", "Film", "Serie"])

if categorie:
    if categorie.lower() == "film":
      
        st.subheader("Recherche par nom")
        nom = st.text_input("Nom du film")
        if nom:
            results = collection.find({"categorie": "film", "titre": {"$regex": nom, "$options": "i"}})
            for result in results:
                st.write(result["titre"],str(result["genre"]),"sorti en ",result["annee"],"en",result["pays"],"est un film qui dure",str(result["duree"]),"minutes .","Le Synopsis en anglais:",result["description"],"Ce film est classé",str(result["rang"]),"eme sur les 250 films les mieux notés sue IMDB")

       
        st.subheader("Recherche par acteur(s)")
        acteurs = st.text_input("Nom des acteurs (séparés par des virgules)")
        if acteurs:
            acteurs_list = [a.strip() for a in acteurs.split(",")]
            results = collection.find({"categorie": "film", "acteurs": {"$in": acteurs_list}})
            for result in results:
                st.write(result["titre"])

   
        st.subheader("Recherche par genre")
        genre = st.selectbox("Genre", ["",'Romance','Drama','Musical','Sport','Family','Adventure','Comedy','Biography','Sci-Fi','Thriller','Horror','ActionWar','Animation','Film-Noir','Music','Fantasy','Western','Crime','Mystery','History'])
        if genre:
            results = collection.find({"categorie": "film", "genre": genre})
            for result in results:
                st.write(result["titre"])

      
        st.subheader("Recherche par durée")
        duree = st.number_input("Durée maximale (en minutes)", min_value=0, max_value=500, value=0)
        if duree:
            results = collection.find({"categorie": "film", "duree": {"$lte": duree}})
            for result in results:
                st.write(result["titre"])

        st.subheader("Recherche par note minimale")
        note = st.number_input("Note minimale (sur 10)", min_value=0, max_value=10, value=0)
        if note:
            results = collection.find({"categorie": "film", "score": {"$gte": note}})
            for result in results:
                st.write(result["titre"])
                
if categorie.lower() == "serie":

    st.subheader("Recherche par nom")
    nom = st.text_input("Nom de la série")
    if nom:
        results = collection.find({"categorie": "serie", "titre": {"$regex": nom, "$options": "i"}})
        for result in results:
            st.write(result["titre"],str(result["genre"]),"sorti en ",result["annee"],"en",result["pays"],"est une série qui dure",str(result["duree"]),"minutes . Avec ",str(result["episodes"]),"épisodes et ",str(result["saisons"]),"saisons","Le Synopsis en anglais :",result["description"],"Cette série est classé",str(result["rang"]),"eme sur les 250 séries les mieux notés su IMDB")

  
    st.subheader("Recherche par acteur(s)")
    acteurs = st.text_input("Nom des acteurs (séparés par des virgules)")
    if acteurs:
        acteurs_list = [a.strip() for a in acteurs.split(",")]
        results = collection.find({"categorie": "serie", "acteurs": {"$in": acteurs_list}})
        for result in results:
            st.write(result["titre"])

  
    st.subheader("Recherche par genre")
    genre = st.selectbox("Genre", ["", "Comedy", "Drama", "Action", "Sci-Fi", "Mystery", "Thriller", "Crime", "Adventure", "Fantasy", "Horror", "Animation"])
    if genre:
        results = collection.find({"categorie": "serie", "genre": genre})
        for result in results:
            st.write(result["titre"])


    st.subheader("Recherche par durée d'épisode")
    duree = st.number_input("Durée maximale d'un épisode (en minutes)", min_value=0, max_value=500, value=0)
    if duree:
        results = collection.find({"categorie": "serie", "duree": {"$lte": duree}})
        for result in results:
            st.write(result["titre"])


    st.subheader("Recherche par note minimale")
    note = st.number_input("Note minimale (sur 10)", min_value=0, max_value=10, value=0)
    if note:
        results = collection.find({"categorie": "serie", "score": {"$gte": note}})
        for result in results:
            st.write(result["titre"])
