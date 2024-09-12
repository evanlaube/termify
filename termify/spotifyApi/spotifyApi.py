from .spotifyAuthorizer import SpotifyAuthorizer
import requests
import json


class SpotifyApi():
    """This class is a wrapper for the Spotify API which carries out all requests to the 
    Spotify API, as well as keeping track of a SpotifyAuthorizer object for maintaining 
    authorization to the API.
    """
    def __init__(self):
        """Constructor method that initializes as SpotifyAuthorizer for maintaining 
        access to the Spotify API and refreshing tokens"""
        self.auth = SpotifyAuthorizer()
        self.auth.refreshToken()
        self.token = self.auth.getToken()

    def makeRequest(self, method, urlEndpoint, body={}):
        """Makes a request to the Spotify API and returns the response, or raises an error 
        if the status code of the response is not 200 or 204
        :param method: Method type. Example 'GET', 'PUT', 'POST'
        :type method: str
        :param urlEndpoint: The part of the request url that comes after 'https://api.spotify.com/v1'
        :type urlEndpoint: str
        :param body: The body of the request
        :type body: dict, optional
        :return: The result of the request that was made
        :rtype: requests.models.Response"""
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

    def play(self, contextURI=None):
        """Set the current playback status to play, and optionally select what media
        to play
        :param contextURI: The URI of the album/playlist/song to play, if excluded, Spotify will
        simply resume playback
        :type contextURI: str, optional
        :return: The result of the PUT request made
        :rtype: requests.models.Response
        """
        body = {}
        if contextURI != None:
            body['context_uri'] = contextURI

        body = json.dumps(body)
        return self.makeRequest('PUT', '/me/player/play', body=body)


    def pause(self):
        """Set the current playback state to pause
        :return: THe result of the PUT request made
        :rtype: requests.models.Response
        """
        return self.makeRequest('PUT', '/me/player/pause')

    def togglePlayback(self):
        """ Sets the current playback state to the opposite of what it currently is.
        Ex: Play -> Pause and Pause -> Play
        :return: The result of the request that is made
        :rtype: requests.models.Response
        """
        state = self.getPlaybackState()
        if state.status_code == 204:
            return None

        if state.json()['is_playing']:
            return self.pause()
        else:
            return self.play()

    def skip(self):
        """Skip the currently playing song
        :return: The result of the request that is made
        :rtype: requests.models.Response
        """
        return self.makeRequest('POST', '/me/player/next')

    def prev(self):
        """Rewind to the beginning of the previous song
        :return: The result of the request that is made
        :rtype: requests.models.Response
        """
        return self.makeRequest('POST', '/me/player/previous')
    
    def getPlaybackState(self):
        """Get the details of the current playback state 
        :return: The current details of the playback state
        :rtype: requests.models.Response 
        """
        return self.makeRequest('GET', '/me/player')

    def setPlaybackDevice(self, deviceId):
        """Sets the active playback device to the input device ID
        :param deviceId: The Spotify given ID of the device to switch the playback to
        :type deviceId: str
        :return: True if the playback was able to be set to the device, False if not
        :rtype: bool
        """
        data = {'device_ids': [deviceId]}
        jsonData = json.dumps(data)
        try:
            self.makeRequest('PUT', '/me/player', body=jsonData)
            return True
        except:
            return False 
        
    def getDevices(self):
        """Gets a list of available playback devices.
        :return: A list of playback devices
        :rtype: dict
        """
        try:
            response = self.makeRequest('GET', '/me/player/devices')
            return response.json()
        except:
            return {} 

    def getCurrentSong(self):
        """Gets the details of the currently playing song or podcast
        :return: Details of current playing song
        :rtype: dict
        """
        try:
            response = self.makeRequest('GET', '/me/player/currently-playing')
            return response.json()
        except:
            return {} 

    def getUserPlaylists(self):
        """Gets the current user's playlists
        :return: The details of the User's playlists
        :rtype: dict
        """
        try:
            response = self.makeRequest('GET', '/me/playlists')
            return response.json()
        except:
            return {} 


