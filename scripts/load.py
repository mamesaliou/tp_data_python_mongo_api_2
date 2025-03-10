from pymongo import MongoClient

def load_data(df):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client.spotify_history
        collection = db.listening_history
        
        data_dict = df.to_dict("records")
        #collection.delete_many({}) # pour éviter de recharger les memes données
        collection.insert_many(data_dict)
        
        # for record in data_dict:
        #     # Utilise un identifiant unique (par exemple, 'id') pour remplacer les documents existants
        #     collection.replace_one({'spotify_track_uri': record['spotify_track_uri']}, record, upsert=True)

        print("Données chargées avec succès dans MongoDB.")
    except Exception as e:
        print(f"Erreur lors du chargement des données dans MongoDB : {e}")

# Utiliser mongosh pour vérifier l'ingestion des données dans MongoDB: 
# docker exec -it mongodb mongosh
