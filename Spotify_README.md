# Visualizing popular Music Genres
_using data provided by Spotify's API_

## Collecting Music Data
If you have ever used [`Spotify`](https://open.spotify.com/), mabye you are familiar with Spotify Wrapped, which tells you stats about the music you have listened to over the past year (such as top genres, songs, amount of hours listened, ect)

Spotify is able to do this with the help of audio models and neural networks to "process raw audio to produce a range of characteristics, including key, tempo, and even loudness"

With the help of an existing python library for interacting with the Spotify API: [`Spotipy`](https://spotipy.readthedocs.io/en/2.18.0/)  
[`Pandas`](https://pandas.pydata.org/) will also aid in collecting the data and visualization

The main charcteristics we will be using today include:  
> `duration_ms`  : duration in miliseconds  
`liveness`  : rated from 0.0 - 1 (how close was this track to being recorded live, measures audience presence)
`energy`  : rated from 0.0 - 1  
`danceability`  : rated from 0.0 - 1  
`loudness`  : measured in dB (measured backwards to prevent audio clipping, closer to 0 meaning louder)  
`mode`  : major/minor (1 = major, 0 = minor)  
`tempo`  : measured in BPM  
`valence`  : rated from 0.0 - 1 (tracks with a higher valence sound more posiive)  
`speechiness`  : rated from 0.0 - 1  
`acousticness`  : a confidence measure of weather a track is acoustic or not

_to find more about how these characteristics are calculated, click [`me`](https://www.theverge.com/tldr/2018/2/5/16974194/spotify-recommendation-algorithm-playlist-hack-nelson)_

To start accessing data from Spotify's API, you will need to create a seperate `.txt` file that contains the following:  
```
client_id ###your id###
client_secret ###your secret###

```

[`Spotify Developer Dashboard`](https://developer.spotify.com/dashboard/login) will provide you with that information if you do not have it already  
_assuming you have a spotify account you can log into_

## What do Genres have in Common?

Using Spotify's preassembed playlists, I choose 8 different genres to compare different tracks characterstics

![dataframes](https://user-images.githubusercontent.com/78603285/118038122-b621a500-b33c-11eb-8f68-b19e89dab4ff.png)

## Visualization

Lets compare the Energy and Danceability using a [`scatterplot`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.plot.scatter.html)!

**Energy and Danceability**

![energy_danceability](https://user-images.githubusercontent.com/78603285/118040221-4cef6100-b33f-11eb-83ad-5b2ed0c5127b.png)

Here, we can see that each genre kind of sticks together, especially `classical`, `latino`, and `metal`  
_across all genres we see that the average energy ranks at about a 0.7 - 0.8, and the same runs true danceability_  

We can conclude that most songs are fairly energetic and danceable 💃

**Energy and Acousticness**

![energy_acousticness](https://user-images.githubusercontent.com/78603285/118043019-d5233580-b342-11eb-93b6-eaa7cf4e8f6d.png)

As expected a softer genre such as `classical` is near the top left and towards the opposite being `metal` near the bottom right. We also see pop staying towards the bottom of the acousticness but staying in the middle of energy. Meanwhile `latino` music has high energy and ranges through acousticness.

Most genres seem to be on the higher energy level with mostly non acoustic songs

**Mode and Tempo**

![mode_tempo](https://user-images.githubusercontent.com/78603285/118043557-888c2a00-b343-11eb-9606-32bb7b1ded80.png)

With 1 meaning "major" and 0 meaning "minor", it is clear to see more songs tend to have their songs in major anywhere from 80 - 180 BPM while minor songs tend to be between 80 - 140 BPM

**Duration and Liveness**

![duration_liveness](https://user-images.githubusercontent.com/78603285/118044198-5c24dd80-b344-11eb-8132-43a150588e30.png)

A strong cluster is near the bottom left corner signifying that the majority of songs and genres are not recorded live and have a duration of around 200,000 miliseconds or 3.3 minutes

**Loudness and Tempo**

![loudess_tempo](https://user-images.githubusercontent.com/78603285/118044821-20d6de80-b345-11eb-8505-ed125bf7170d.png)

Almost all genres excluding `classical` have a dB level of around -3 and -10, the closer it is to 0 meaning louder, which is not suprising for `classical` being the quietest with slow tempos.

However even though almost all genres are on the louder side, the tempo is very diverse with the average tempo coming in about 122 BPM

**Valence and Loudness**

![Valence_Loudness](https://user-images.githubusercontent.com/78603285/118046279-17e70c80-b347-11eb-98ac-2ee7a9758093.png)

Again we see a simlar chart as above with the loudness however with valence on the y-axis you can see a bit more genre separation such as with `metal` and `latino`, with `latino` clumping together towards the top signifiying a lot of their music is loud and happy. 

**Valence and Speechiness**

![Valence_Speechiness](https://user-images.githubusercontent.com/78603285/118046778-cdb25b00-b347-11eb-9238-d971db3d1a2a.png)

When it comes to speechiness, most songs are well music so they will fall below the 0.3 marker exept for some outliers which mainly include `rap`, we can also see that `edm` stays near the left.

**How can I use this data?**

Although it is facinating to see what trends genres do or don't follow, an uncoming artist will be able to look at these trends to see what the big players in their desired genres are doing.

For example:

>Lets take an aspiring metal band, looking at the trends metal music seems to be highly energetic throughout any BPM, the majority written in a minor key, and slightly longer than the average song (more than the 3 minute mark).

Disregarding genre, overall trends include:
* the duration of songs generally fall between 1 - 5 minutes
* usually recorded in a studio (not live)
* the mean tempo is around 120
* loudness ranges anywhere between 0 and -10 dBs
