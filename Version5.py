import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials
client_id = '56d3570df22c40339c679a173cbdd917'
client_secret = '96c06f0548ef47229643d69f32a81481'

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get the artist's top tracks
def get_top_tracks(artist_id):
    results = sp.artist_top_tracks(artist_id)
    tracks = results['tracks']
    return [(track['id'], track['name']) for track in tracks[:5]]  # Limiting to 5 tracks

# Function to get the track's popularity by country
def get_track_popularity(track_id):
    track_info = sp.track(track_id)
    popularity_by_country = {}
    for available_market in track_info['available_markets']:
        track_info_country = sp.track(track_id, market=available_market)
        popularity_by_country[available_market] = track_info_country['popularity']
    return popularity_by_country

# Specify the artist you're interested in
artist_name = 'Elton John'

# Search for the artist and retrieve their ID
results = sp.search(q='artist:' + artist_name, type='artist')
items = results['artists']['items']
if len(items) > 0:
    artist_id = items[0]['id']
else:
    print("Artist not found.")

# Get the artist's top tracks
top_tracks = get_top_tracks(artist_id)

# Create an empty DataFrame to store the results
df = pd.DataFrame(columns=['Country', 'Track', 'Popularity'])

# Iterate over the top tracks and get the popularity by country
for track_id, track_name in top_tracks:
    popularity_by_country = get_track_popularity(track_id)
    for country, popularity in popularity_by_country.items():
       new_row = pd.DataFrame({'Country': [country], 'Track': [track_name], 'Popularity': [popularity]})
       df = pd.concat([df, new_row], ignore_index=True)

# Print the resulting DataFrame
print(df)
