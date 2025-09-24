from flask import Blueprint, jsonify, request
import requests
import json
import uuid
from app import dynamo
# from app import redis


top_ten_bp = Blueprint("top_ten", __name__, url_prefix="/api/v1/top_ten")
credentials = {}
with open('app/configs/credentials.json', 'r') as file:
    credentials = json.load(file)
BASE_HEADERS = {'Authorization': f'Bearer {credentials["token"]}'}
BASE_URL = "https://api.genius.com"

@top_ten_bp.route("", methods=["POST"])
def get_top_ten():
    
    data = request.get_json()
    artist_id = data.get('id')
    use_cache = False if request.args.get('use_cache') == "False" else True
    print(use_cache)

    if dynamo.check_artist_dynamo(artist_id) and use_cache:
        # GET DATA FROM REDIS THEN RETURN IT
        return jsonify([{"found": "data"}]), 200

    artist_data = get_artist_id(artist_id)
    songs = get_songs(artist_data["name"])
    result = process_list_songs(songs)

    if not use_cache:
        # DELETE FROM REDIS
        dynamo.delete_artist(artist_id)

    item = {
        "artist_id": artist_id,
        "transaction_id": str(uuid.uuid4()),
        "artist_name": artist_data["name"]
    }
    d_resp = dynamo.dynamo_insert(item)
    # INSERT DATA ON REDIS 

    return jsonify(result), 200

def get_artist_id(id: str) -> dict:
    """
    receives artist id then return an object with all data
    """
    url = f"{BASE_URL}/artists/{id}"

    response = requests.get(url, headers=BASE_HEADERS)

    if response.status_code == 200:
        return response.json()["response"]["artist"]
    
    else:
        return None

def get_songs(artists: str) -> list: 
    """
    receives artists name then returns a list of songs
    """
    url = f"{BASE_URL}/search"
    params = {"q": artists}

    response = requests.get(params=params, url=url, headers=BASE_HEADERS)

    if response.status_code == 200:
        return response.json()["response"]["hits"]
    
    else:
        return None
    
def process_list_songs(songs: list) -> list:
    """
    receives a list of songs then return a top ten list sorted by 'pageviews'
    """
    hash_map = {}
    for song in songs:
        exist = song["result"]["stats"]["pageviews"]
        if not hash_map.get(exist):
            hash_map[exist] = [song]
        else:
            hash_map[exist].append(song)
    
    sorted_keys = sorted(hash_map.keys())
    return_list = []

    while len(return_list) < 10 and len(sorted_keys) > 0:
        p_key = sorted_keys.pop()
        for s in hash_map[p_key]:
            return_list.append(s)

    return return_list

        

