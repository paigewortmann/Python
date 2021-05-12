# -*- coding: utf-8 -*-
"""
Created on Mon May 10 20:07:05 2021

@author: 17244
"""

# -*- coding: utf-8 -*-
"""
Created on Sun May  9 01:42:50 2021

@author: 17244
"""
import spotipy
spotify = spotipy.Spotify()
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials


def get_spotify_credentials(filename):
    '''connecting to the Spotify API'''
    if filename is None:
        raise IOError('Credentials file is none.')

    f = open(filename)

    txt = f.readlines()
    client_id = '80362f47e52c4b55bfe16b8479734e86'
    client_secret = '8228900b04aa4effba6ae6aa24fc3ed8'
    for l in txt:
        l = l.replace('\n', '').split(' ')
        if l[0] == 'client_id':
            client_id = l[1]
        elif l[0] == 'client_secret':
            client_secret = l[1]

    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    sp.trace = True

    return sp

def get_spotify_data(artist_name, credentials_file):
    '''will return data reguarding each track within a playlist'''

    # get authorisation stuff
    sp = get_spotify_credentials(credentials_file)

    # first get spotify artist uri
    results = sp.search(q='artist:' + artist_name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]

    uri = artist['uri']

    # now get album uris
    results = sp.artist_albums(uri, album_type='album')
    albums = results['items']
    while results['next']:
        results = sp.next(results)
        albums.extend(results['items'])

    uris = []
    track_names = []
    album_names = []

    # get track data
    for album in albums:
        for t in sp.album(album['uri'])['tracks']['items']:
            uris.append(t['uri'])
            track_names.append(t['name'])
            album_names.append(album['name'])
    features = []
    for i in range(len(uris)// 100 + 1):
        fs = sp.audio_features(uris[i*100:min((i+1)*100, len(uris))])
        if fs[0] is not None:
            features.extend(fs)

    # make dataframe
    dat = pd.DataFrame(features)
    dat['track_name'] = track_names
    dat['album'] = album_names
    dat['artists'] = artist_name

    # ignore live, remix and deluxe album versions
    mask = [('live' not in s.lower() and 'deluxe' not in s.lower() 
             and 'remix' not in s.lower() and 'rmx' not in s.lower()
            and 'remastered' not in s.lower()) for s in dat.album.values]
    dat = dat[mask]
    mask2 = [(('remix' not in s.lower()) and 
              'remastered' not in s.lower() and 'live' not in s.lower()
             and 'version' not in s.lower()) for s in dat.track_name.values]
    dat = dat[mask2]

    dat.set_index('track_name', inplace=True)
    dat.drop_duplicates(inplace=True)
    dat = dat[~dat.index.duplicated(keep='first')]

    return dat

# taking in various spotify playlists and storing via csv
indie = get_spotify_data('Ultimate Indie', 'credentials.txt')
indie.to_csv(r'C:\Users\17244\Python2_git\python2_git\spotify_genres_csv\indie.csv', index = False)

country = get_spotify_data('Hot Country', 'credentials.txt')
country.to_csv(r'C:\Users\17244\Python2_git\python2_git\spotify_genres_csv\country.csv', index = False)

pop = get_spotify_data('Viral Hits', 'credentials.txt')
pop.to_csv(r'C:\Users\17244\Python2_git\python2_git\spotify_genres_csv\pop.csv', index = False)

metal = get_spotify_data('Metal', 'credentials.txt')
metal.to_csv(r'C:\Users\17244\Python2_git\python2_git\spotify_genres_csv\metal.csv', index = False)

edm = get_spotify_data('Edm', 'credentials.txt')
edm.to_csv(r'C:\Users\17244\Python2_git\python2_git\spotify_genres_csv\edm.csv', index = False)

rap = get_spotify_data('Rap Caviar', 'credentials.txt')
rap.to_csv(r'C:\Users\17244\Python2_git\python2_git\spotify_genres_csv\rap.csv', index = False)

classical = get_spotify_data('classical', 'credentials.txt')
classical.to_csv(r'C:\Users\17244\Python2_git\python2_git\spotify_genres_csv\classical.csv', index = False)

latino = get_spotify_data('latino', 'credentials.txt')
latino.to_csv(r'C:\Users\17244\Python2_git\python2_git\spotify_genres_csv\latino.csv', index = False)


def get_spotify_playlist_data(username='spotify', playlist=None, credentials_file=None):
    '''grabs artist, tracks, and IDs'''

    # set a limit to total number of tracks to analyse
    track_number_limit = 500

    # get authorisation stuff
    sp = get_spotify_credentials(credentials_file)

    # get user playlists
    p = None
    results = sp.user_playlists(username)
    playlists = results['items']

    if playlist is None: # use first of the user's playlists
        playlist = playlists[0]['name']

    for pl in playlists:
        if pl['name'] is not None and pl['name'].lower() == playlist.lower():
            p = pl
            break
    while results['next'] and p is None:
        results = sp.next(results)
        playlists = results['items']
        for pl in playlists:
            if pl['name'] is not None and pl['name'].lower() == playlist.lower():
                p = pl
                break

    if p is None:
        print('Could not find playlist')
        return

    results = sp.user_playlist(p['owner']['id'], p['id'], fields="tracks,next")['tracks']
    tracks = results['items']
    while results['next'] and len(tracks) < track_number_limit:
        results = sp.next(results)
        if results['items'][0] is not None:
            tracks.extend(results['items'])

    ts = []
    track_names = []

    for t in tracks:
        track = t['track']
        track['album'] = track['album']['name']
        track_names.append(t['track']['name'])
        artists = []
        for a in track['artists']:
            artists.append(a['name'])
        track['artists'] = ', '.join(artists)
        ts.append(track)

    dat = pd.DataFrame(ts)

    dat.drop(['available_markets', 'disc_number', 'external_ids', 'external_urls'], axis=1, inplace=True)

    features = []
    # loop to take advantage of spotify being able to get data for 100 tracks at once
    for i in range(len(dat)// 100 + 1):
        fs = sp.audio_features(dat.uri.iloc[i*100:min((i+1)*100, len(dat))])
        if fs[0] is not None:
            features.extend(fs)

    fs = pd.DataFrame(features)

    dat = pd.concat([dat, fs], axis=1)
    dat['track_name'] = track_names

    # ignore live, remix and deluxe album versions
    mask = [(('live' not in s.lower()) and ('deluxe' not in s.lower())
             and ('remix' not in s.lower())) for s in dat.album.values]
    dat = dat[mask]
    mask2 = [(('remix' not in s.lower()) and
              'remastered' not in s.lower()
             and 'version' not in s.lower()) for s in dat.track_name.values]
    dat = dat[mask2]

    dat.set_index('track_name', inplace=True)
    dat = dat[~dat.index.duplicated(keep='first')]
    dat = dat.T[~dat.T.index.duplicated(keep='first')].T

    return dat


# making data frames from reading the CSVs using pandas
dfs = {'indie': pd.read_table('indie.csv'), 'pop': pd.read_table('pop.csv'), 'country': pd.read_table('country.csv'),
       'metal': pd.read_table('metal.csv'), 'edm': pd.read_table('edm.csv'), 'rap': pd.read_table('rap.csv'),
       'classical': pd.read_table('classical.csv'), 'latino': pd.read_table('latino.csv')}


frames = [indie, pop, country, metal, edm, rap, classical, latino]
result = pd.concat(frames) # merging all the dataframes into one big dataframe

def tempo_loud():
    '''scatter plot with tempo vs loudness'''
    ax = indie.plot(kind='scatter', x='loudness', y='tempo',
                    color= 'Blue', label = 'Indie', title= 'Tempo vs. Loudness',
                    figsize= (9,8));
    
    country.plot(kind='scatter', x='loudness', y='tempo',
                 color= 'gold', label= 'Country', ax=ax);
    
    pop.plot(kind='scatter', x='loudness', y='tempo',
                 color= 'green', label= 'pop', ax=ax);
    
    metal.plot(kind='scatter', x='loudness', y='tempo',
                 color= 'red', label= 'metal', ax=ax);
    
    edm.plot(kind='scatter', x='loudness', y='tempo',
               color= 'black', label= 'edm', ax=ax);
    
    rap.plot(kind='scatter', x='loudness', y='tempo',
               color= 'olive', label= 'rap', ax=ax);

    classical.plot(kind='scatter', x='loudness', y='tempo',
               color= 'magenta', label= 'classical', ax=ax);
    
    latino.plot(kind='scatter', x='loudness', y='tempo',
               color= 'lightsteelblue', label= 'latino', ax=ax);
    
    
def dance_energy():
    '''scatter plot with energy and danceability'''
    ax = indie.plot(kind='scatter', x='energy', y='danceability',
                    color= 'Blue', label = 'Indie', title= 'Energy vs. Danceability',
                    figsize= (9,8));
    
    country.plot(kind='scatter', x='energy', y='danceability',
                 color= 'gold', label= 'Country', ax=ax);
    
    pop.plot(kind='scatter', x='energy', y='danceability',
                 color= 'green', label= 'pop', ax=ax);
    
    metal.plot(kind='scatter', x='energy', y='danceability',
                 color= 'red', label= 'metal', ax=ax);
    
    edm.plot(kind='scatter', x='energy', y='danceability',
               color= 'black', label= 'edm', ax=ax);
    
    rap.plot(kind='scatter', x='energy', y='danceability',
               color= 'olive', label= 'rap', ax=ax);

    classical.plot(kind='scatter', x='energy', y='danceability',
               color= 'magenta', label= 'classical', ax=ax);
    
    latino.plot(kind='scatter', x='energy', y='danceability',
               color= 'lightsteelblue', label= 'latino', ax=ax);
    
def valence_duration():
    '''scatter plot with valence and speechiness'''
    ax = indie.plot(kind='scatter', x='speechiness', y='valence',
                    color= 'Blue', label = 'Indie', title= 'Valence vs. Speechiness',
                    figsize= (9,8));
    
    country.plot(kind='scatter', x='speechiness', y='valence',
                 color= 'gold', label= 'Country', ax=ax);
    
    pop.plot(kind='scatter', x='speechiness', y='valence',
                 color= 'green', label= 'pop', ax=ax);
    
    metal.plot(kind='scatter', x='speechiness', y='valence',
                 color= 'red', label= 'metal', ax=ax);
    
    edm.plot(kind='scatter', x='speechiness', y='valence',
               color= 'black', label= 'edm', ax=ax);
    
    rap.plot(kind='scatter', x='speechiness', y='valence',
               color= 'olive', label= 'rap', ax=ax);

    classical.plot(kind='scatter', x='speechiness', y='valence',
               color= 'magenta', label= 'classical', ax=ax);
    
    latino.plot(kind='scatter', x='speechiness', y='valence',
               color= 'lightsteelblue', label= 'latino', ax=ax);
    
def loud_valence():
    '''scatter plot with valence and speechiness'''
    ax = indie.plot(kind='scatter', x='loudness', y='valence',
                    color= 'Blue', label = 'Indie', title= 'Valence vs. Loudness',
                    figsize= (9,8));
    
    country.plot(kind='scatter', x='loudness', y='valence',
                 color= 'gold', label= 'Country', ax=ax);
    
    pop.plot(kind='scatter', x='loudness', y='valence',
                 color= 'green', label= 'pop', ax=ax);
    
    metal.plot(kind='scatter', x='loudness', y='valence',
                 color= 'red', label= 'metal', ax=ax);
    
    edm.plot(kind='scatter', x='loudness', y='valence',
               color= 'black', label= 'edm', ax=ax);
    
    rap.plot(kind='scatter', x='loudness', y='valence',
               color= 'olive', label= 'rap', ax=ax);

    classical.plot(kind='scatter', x='loudness', y='valence',
               color= 'magenta', label= 'classical', ax=ax);
    
    latino.plot(kind='scatter', x='loudness', y='valence',
               color= 'lightsteelblue', label= 'latino', ax=ax);

def duration_liveness():
    '''scatter plot with duration and liveness'''
    ax = indie.plot(kind='scatter', x='duration_ms', y='liveness',
                    color= 'Blue', label = 'Indie', title= 'Duration vs. Liveness',
                    figsize= (9,8));
    
    country.plot(kind='scatter', x='duration_ms', y='liveness',
                 color= 'gold', label= 'Country', ax=ax);
    
    pop.plot(kind='scatter', x='duration_ms', y='liveness',
                 color= 'green', label= 'pop', ax=ax);
    
    metal.plot(kind='scatter', x='duration_ms', y='liveness',
                 color= 'red', label= 'metal', ax=ax);
    
    edm.plot(kind='scatter', x='duration_ms', y='liveness',
               color= 'black', label= 'edm', ax=ax);
    
    rap.plot(kind='scatter', x='duration_ms', y='liveness',
               color= 'olive', label= 'rap', ax=ax);

    classical.plot(kind='scatter', x='duration_ms', y='liveness',
               color= 'magenta', label= 'classical', ax=ax);
    
    latino.plot(kind='scatter', x='duration_ms', y='liveness',
               color= 'lightsteelblue', label= 'latino', ax=ax);
    
def acousticness_energy():
    '''scatter plot with energy and acousticness'''
    ax = indie.plot(kind='scatter', x='energy', y='acousticness',
                    color= 'Blue', label = 'Indie', title= 'Energy vs. Acousticness',
                    figsize= (9,8));
    
    country.plot(kind='scatter', x='energy', y='acousticness',
                 color= 'gold', label= 'Country', ax=ax);
    
    pop.plot(kind='scatter', x='energy', y='acousticness',
                 color= 'green', label= 'pop', ax=ax);
    
    metal.plot(kind='scatter', x='energy', y='acousticness',
                 color= 'red', label= 'metal', ax=ax);
    
    edm.plot(kind='scatter', x='energy', y='acousticness',
               color= 'black', label= 'edm', ax=ax);
    
    rap.plot(kind='scatter', x='energy', y='acousticness',
               color= 'olive', label= 'rap', ax=ax);

    classical.plot(kind='scatter', x='energy', y='acousticness',
               color= 'magenta', label= 'classical', ax=ax);
    
    latino.plot(kind='scatter', x='energy', y='acousticness',
               color= 'lightsteelblue', label= 'latino', ax=ax);

def mode_tempo():
    ''''scatter plot with mode(major= 1 and minor= 0) and tempo '''
    ax = indie.plot(kind='scatter', x='tempo', y='mode',
                    color= 'Blue', label = 'Indie', title= 'Mode vs. Tempo',
                    figsize= (9,8));
    
    country.plot(kind='scatter', x='tempo', y='mode',
                 color= 'gold', label= 'Country', ax=ax);
    
    pop.plot(kind='scatter', x='tempo', y='mode',
                 color= 'green', label= 'pop', ax=ax);
    
    metal.plot(kind='scatter', x='tempo', y='mode',
                 color= 'red', label= 'metal', ax=ax);
    
    edm.plot(kind='scatter', x='tempo', y='mode',
               color= 'black', label= 'edm', ax=ax);
    
    rap.plot(kind='scatter', x='tempo', y='mode',
               color= 'olive', label= 'rap', ax=ax);

    classical.plot(kind='scatter', x='tempo', y='mode',
               color= 'magenta', label= 'classical', ax=ax);
    
    latino.plot(kind='scatter', x='tempo', y='mode',
               color= 'lightsteelblue', label= 'latino', ax=ax);
    
def loud_liveness():
    '''scatter plot with loudness and liveness'''
    ax = indie.plot(kind='scatter', x='loudness', y='liveness',
                    color= 'Blue', label = 'Indie', title= 'Loudness vs. Liveness',
                    figsize= (9,8));
    
    country.plot(kind='scatter', x='loudness', y='liveness',
                 color= 'gold', label= 'Country', ax=ax);
    
    pop.plot(kind='scatter', x='loudness', y='liveness',
                 color= 'green', label= 'pop', ax=ax);
    
    metal.plot(kind='scatter', x='loudness', y='liveness',
                 color= 'red', label= 'metal', ax=ax);
    
    edm.plot(kind='scatter', x='loudness', y='liveness',
               color= 'black', label= 'edm', ax=ax);
    
    rap.plot(kind='scatter', x='loudness', y='liveness',
               color= 'olive', label= 'rap', ax=ax);

    classical.plot(kind='scatter', x='loudness', y='liveness',
               color= 'magenta', label= 'classical', ax=ax);
    
    latino.plot(kind='scatter', x='loudness', y='liveness',
               color= 'lightsteelblue', label= 'latino', ax=ax);
    



def main():
    
    tempo_loud()
    dance_energy()
    valence_duration()
    loud_valence()
    duration_liveness()
    acousticness_energy()
    mode_tempo()
    loud_liveness()
    
    
if __name__ == "__main__":
    main()
