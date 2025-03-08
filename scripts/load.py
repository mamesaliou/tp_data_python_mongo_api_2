# from pymongo import MongoClient

# def load_data(df, db_name, collection_name):
#     client = MongoClient("mongodb://localhost:27017/")
#     db = client[db_name]
#     collection = db[collection_name]
    
#     data_dict = df.to_dict("records")
#     collection.insert_many(data_dict)

from pymongo import MongoClient, errors

def load_data(df, db_name, collection_name):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client[db_name]
        collection = db[collection_name]
        
        data_dict = df.to_dict("records")
        collection.insert_many(data_dict)
        
        print("Data inserted successfully")
    except errors.ServerSelectionTimeoutError as sste:
        print("Server selection error: Unable to connect to MongoDB server.")
        print(sste)
    except errors.ConnectionFailure as cf:
        print("Connection failure: Failed to connect to MongoDB server.")
        print(cf)
    except errors.PyMongoError as pme:
        print("PyMongo error occurred.")
        print(pme)
    except Exception as e:
        print("An unexpected error occurred.")
        print(e)

# Example usage
# load_data(your_dataframe, 'your_db_name', 'your_collection_name')
