from .spotifyAuthorizer import SpotifyAuthorizer
import requests
import json

CLIENT_ID = '07974f405e584de8b13f8b32e9c7ea8a'

class SpotifyApi():
    def __init__(self):
        self.auth = SpotifyAuthorizer()
        self.auth.refreshToken()
        self.token = self.auth.getToken()

    def makeRequest(self, method, urlEndpoint, body={}):
        if(self.auth.tokenExpired()):
            self.auth.refreshToken()

        headers = {'Authorization': f'Bearer {self.token}'}

        if urlEndpoint[0] != '/':
            urlEndpoint = '/' + urlEndpoint

        url = f'https://api.spotify.com/v1' + urlEndpoint

        response = requests.request(method, url, headers=headers, data=body)

        if response.status_code not in (200, 204):
            raise Exception(f"Request failed with status code {response.status_code}: {response.text}")

        return response

    def play(self):
        return self.makeRequest('PUT', '/me/player/play')


    def pause(self):
        return self.makeRequest('PUT', '/me/player/pause')

    def togglePlayback(self):
        state = self.getPlaybackState()
        if state.status_code == 204:
            self.resetPlayback()

        if state.json()['is_playing']:
            return self.pause()
        else:
            return self.play()

    def skip(self):
        return self.makeRequest('POST', '/me/player/next')

    def prev(self):
        return self.makeRequest('POST', '/me/player/previous')
    
    def getPlaybackState(self):
        return self.makeRequest('GET', '/me/player')

    def resetPlayback(self):
        devices = self.getDevices()

        if devices == None:
            return False

        id = None
        for device in devices['devices']:
            if device['is_active']:
                id = device['id']

        if id == None:
            #TODO: find a way to resume playback on most recent device / set a default device
            raise Exception("No active playback device")

        self.setPlaybackDevice(id)
        
    def setPlaybackDevice(self, deviceId):
        data = {'device_ids': [deviceId]}
        jsonData = json.dumps(data)
        try:
            self.makeRequest('PUT', '/me/player', body=jsonData)
            return True
        except:
            return False 
        
    def getDevices(self):
        try:
            response = self.makeRequest('GET', '/me/player/devices')
            return response.json()
        except:
            return None

    def getCurrentSong(self):
        try:
            response = self.makeRequest('GET', '/me/player/currently-playing')
            return response.json()
        except:
            return None 


