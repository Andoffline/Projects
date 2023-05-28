import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd

# Spotify API credentials
client_id = '56d3570df22c40339c679a173cbdd917'
client_secret = '96c06f0548ef47229643d69f32a81481'

# Initialize Spotipy client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get the popularity of a track in each country
def get_track_popularity(track_id):
    track_info = sp.track(track_id)
    popularity_by_country = {}
    for market in track_info['available_markets']:
        track = sp.track(track_id, market=market)
        popularity_by_country[market] = track['popularity']
    return popularity_by_country

# Specify the track you're interested in
track_id = 'https://open.spotify.com/track/0WPYdlA05STEYRYVpBpcW3?si=9bbba94770014018'

# Get the popularity of the track in each country
popularity_by_country = get_track_popularity(track_id)

# Create a DataFrame to store the results
df = pd.DataFrame(popularity_by_country.items(), columns=['Country', 'Popularity'])

# Sort the DataFrame by popularity in descending order
df.sort_values('Popularity', ascending=False, inplace=True)

# Reset the index of the DataFrame
df.reset_index(drop=True, inplace=True)

# Print the resulting DataFrame
print(df)
