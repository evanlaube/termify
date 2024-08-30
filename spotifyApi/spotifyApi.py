from .spotifyAuthorizer import SpotifyAuthorizer

import requests

CLIENT_ID = '07974f405e584de8b13f8b32e9c7ea8a'

class SpotifyApi():
    def __init__(self):
        self.auth = SpotifyAuthorizer()
        self.auth.refreshToken()
        self.token = self.auth.getToken()

    def makeRequest(self, method, urlEndpoint):
        if(self.auth.tokenExpired()):
            self.auth.refreshToken()

        headers = {'Authorization': f'Bearer {self.token}'}

        if urlEndpoint[0] != '/':
            urlEndpoint = '/' + urlEndpoint

        url = f'https://api.spotify.com/v1' + urlEndpoint

        response = requests.request(method, url, headers=headers)

        if response.status_code not in (200, 204):
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        return response

    def play(self):
        self.makeRequest('PUT', '/me/player/play')

    def pause(self):
        self.makeRequest('PUT', '/me/player/pause')
