from pymongo import MongoClient, errors

def load_data(df, db_name, collection_name):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client[db_name]
        collection = db[collection_name]
        
        data_dict = df.to_dict("records")
        collection.insert_many(data_dict)
        
    print("Données chargées avec succès dans MongoDB.")
    except Exception as e:
        print(f"Erreur lors du chargement des données dans MongoDB : {e}")

# Example usage
# load_data(your_dataframe, 'your_db_name', 'your_collection_name')
# Utiliser mongosh pour vérifier l'ingestion des données dans MongoDB: 
# docker exec -it mongodb mongosh
