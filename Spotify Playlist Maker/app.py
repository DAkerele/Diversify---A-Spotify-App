import json
import random
import requests
from bs4 import BeautifulSoup
from secrets import spotify_user_id, spotify_token

class Playlist:
    def __init__(self, key=None, genre="mix",name="tasty lick"):
        self._key = key
        self._genre = genre
        self.assocations = []
        self.playlist = None
        self._base_url = "https://api.spotify.com/v1"
        self.scrap_url = "https://wordassociations.net/en/words-associated-with/"+key+"?start=0"
        self.user_id = spotify_user_id
        self.token = spotify_token
        self.name = name

    '''
    def create_association(self):
        response = requests.get(self.scrap_url)
        soup = BeautifulSoup(response.content, "html.parser")
        words = soup.select(".NOUN-SECTION, .ADJECTIVE-SECTION, .VERB-SECTION")
        print(words.prettify())
        print("creating word association list")
        for item in words.find_all('a'):
            print(item.get_text())
            self.assocations.append(item.get_text())

        print("word association list complete")
    '''

    def intialize_playlist(self):#creates an empty playlist
        request_body = json.dumps({
            "name" : self.name,
            "description": "fresh out the oven",
            "public": True
        })

        query = self._base_url +"/users/{}/playlists".format(self.user_id)
        response = requests.post(
            query,
            data = request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization" : "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()

        self.playlist = response_json['id']




    def find_playlists(self,limit):#returns a list of playlists ids from query
        query = "https://api.spotify.com/v1/search?q="+self._key+" "+self._genre+"&type=playlist&limit="+str(limit)+"&market=US"
        playlists = []
        response = requests.get(query,
            headers = {
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()

        for key in response_json['playlists']['items']:
            playlists.append(key['id'])

        return playlists


    def _extract_songs(self, playlist):#returns a list of track objects from playlist
        songs = []
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist)
        response = requests.get(query,
            headers = {
                "Authorization": "Bearer {}".format(self.token)
            }
        )
        response_json = response.json()
        for obj in response_json['items']:
            songs.append(obj['track'])

        return songs

    def _check_genre(self,track):#returns an array of genres artist performs in
        artist_id = track['artists'][0]['id']
        query = "https://api.spotify.com/v1/artists/{}".format(artist_id)
        response = requests.get(query,
            headers = {
                "Authorization": "Bearer {}".format(self.token)
            }
        )

        response_json = response.json()
        return response_json['genres']



    def add_song(self, song):#adds song to playlist
        query = "https://api.spotify.com/v1/playlists/{}/tracks".format(self.playlist)
        request_body = json.dumps([song['uri']])

        response = requests.post(query,
            data= request_body,
            headers={
                "Content-Type": "application/json",
                "Authorization" : "Bearer {}".format(self.token)
            }
        )
        print(response)
        return response.json()



    def generate(self, size):#curates a playlist
        self.intialize_playlist()
        playlist_query = self.find_playlists(5)
        curr_size = 0
        added_songs = {}
        while curr_size < size:
            playlist = random.choice(playlist_query)
            print(playlist)
            songs = self._extract_songs(playlist)
            random_song_number = random.randint(1,3)
            i = 0
            while i < random_song_number:
                track = random.randint(0,len(songs)-1)
                if(track in added_songs):
                    pass
                else:
                    genre_string = str(self._check_genre(songs[track]))
                    print(genre_string)
                    if(genre_string.find(self._genre) != -1):
                        self.add_song(songs[track])
                        added_songs[track] = songs[track]
                        curr_size+=1
                        #print(curr_size)
                        i+=1


 



def main():
    
main()
