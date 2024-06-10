import os
import urllib.parse
import logging

from flask import Flask, jsonify
from dotenv import load_dotenv, find_dotenv

from spotipy import Spotify, SpotifyClientCredentials

load_dotenv(dotenv_path=find_dotenv())

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_URI = os.getenv("SPOTIFY_URI", 'https://open.spotify.com/search/')
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", 8080)

if not SPOTIFY_CLIENT_SECRET or not SPOTIFY_CLIENT_ID:
    logging.error("No Spotify client ID provided, please check your environment variables.")
    exit(1)

sp = Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET))

app = Flask(__name__)


def get_track_info(track_id):
    track_info = sp.track(track_id)
    return {
        "title": track_info.get("name"),
        "artist": '; '.join(artist['name'] for artist in track_info.get("artists", []))
    }


@app.route('/')
def index():
    return "<h1>MusicSharer. Endpoints:</h1><ul><li>/track/&lt;track_id&gt;</li></ul>"


@app.route('/track/<track_id>')
def get_track_data(track_id):
    track_info = get_track_info(track_id)
    track_info.update({"search_url": SPOTIFY_URI + urllib.parse.quote_plus('{title} {artist}'.format(**track_info))})

    return jsonify(track_info)


if __name__ == "__main__":
    app.run(host=HOST, port=PORT)
