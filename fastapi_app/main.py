from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
# from scripts.extract import extract_data
# from scripts.transform import transform_data
# from scripts.load import load_data

# file_path = './data/spotify_history.csv'
# df = extract_data(file_path)
# df = transform_data(df)
# load_data(df)

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client.spotify_history
collection = db.listening_history

class History(BaseModel):
    spotify_track_uri: str
    ts: str
    artist_name: str
    track_name: str
    ms_played: int
    platform: str
    reason_start: str
    reason_end: str
    shuffle: bool
    skipped: bool
    minutes_played: float
    day_of_week: str
    hour_of_day: int

@app.post("/history/")
def create_history(history: History):
    result = collection.insert_one(history.dict())
    return {"id": str(result.inserted_id)}

@app.get("/history/")
def read_history():
    try:
        history = list(collection.find().limit(10))
        for record in history:
            record["id"] = str(record["_id"])
            del record["_id"]
        return history
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/history/{id}")
def read_history_id(id: str):
    try:
        history = collection.find_one({"_id": ObjectId(id)})
        if history is None:
            raise HTTPException(status_code=404, detail="History not found")
        history["id"] = str(history["_id"])
        del history["_id"]
        return history
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/history/{id}")
def update_history(id: str, history: History):
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": history.dict()})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="History not found")
    return {"message": "History updated"}

@app.delete("/history/{id}")
def delete_history(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="History not found")
    return {"message": "History deleted"}

@app.get("/top-artists/")
def top_artists():
    pipeline = [
        {"$group": {"_id": "$artist_name", "total_ms_played": {"$sum": "$ms_played"}}},
        {"$sort": {"total_ms_played": -1}},
        {"$limit": 10}
    ]
    top_artists = list(collection.aggregate(pipeline))
    return top_artists

@app.get("/top-tracks/")
def top_tracks():
    pipeline = [
        {"$group": {"_id": "$track_name", "total_ms_played": {"$sum": "$ms_played"}}},
        {"$sort": {"total_ms_played": -1}},
        {"$limit": 10}
    ]
    top_tracks = list(collection.aggregate(pipeline))
    return top_tracks

@app.get("/top-albums/")
def top_albums():
    pipeline = [
        {"$group": {"_id": "$album_name", "total_ms_played": {"$sum": "$ms_played"}}},
        {"$sort": {"total_ms_played": -1}},
        {"$limit": 10}
    ]
    top_albums = list(collection.aggregate(pipeline))
    return top_albums

@app.get("/skipped-ratio/")
def skipped_ratio():
    pipeline = [
        {"$group": {"_id": None, "skipped_ratio": {"$avg": {"$cond": ["$skipped", 1, 0]}}}}
    ]
    skipped_ratio = list(collection.aggregate(pipeline))
    return skipped_ratio[0]

@app.get("/listening-time-per-day/")
def listening_time_per_day():
    pipeline = [
        {"$group": {"_id": "$day_of_week", "total_ms_played": {"$sum": "$ms_played"}}},
        {"$sort": {"_id": 1}}
    ]
    listening_time_per_day = list(collection.aggregate(pipeline))
    return listening_time_per_day
