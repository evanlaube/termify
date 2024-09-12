
import os
import base64
import hashlib
import hashlib
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import webbrowser
from dotenv import set_key, get_key
from time import time
import os
from pathlib import Path

REDIRECT_URI = 'http://localhost:8888/callback'
envPath = Path(os.getenv('TERMIFY_ENV_PATH', Path.home() / '.termify' / '.env'))

class SpotifyAuthorizer:
    """This class manages maintaining authorization to the Spotify API using PKCE. 
    The Spotify Client ID, Access Token, and other details are stored in the .env 
    file in the environment path"""

    def __init__(self):
        """Constructor method
        """

        self.clientId = get_key(envPath, 'TFY_CLIENT_ID')

        if self.clientId == None:
            raise Exception("Authorization Error: TFY_CLIENT_ID not defined in" + str(envPath))

    def refreshToken(self):
        """Send a request to the Spotify API to refresh the current access token, if it 
        has expired. If there is no token, it simply requests a new token from the API"""
        if get_key(envPath, 'TFY_ACCESS_TOKEN') == None:
            self.requestAuth()
        else:
            if self.tokenExpired():
                self._refreshAccessToken()

        self.token = get_key(envPath, 'TFY_ACCESS_TOKEN')

    def requestAuth(self):
            """Saves an access token to the Spotify API. This token is generated using 
            PKCE authorization, and needs a web browser login to Spotify to function."""
            secret = self._genPkceCodeVerifier()
            challenge = self._genPkceChallenge(secret)
            authUrl = self._getAuthorizationUrl(challenge)
            webbrowser.open(authUrl)
            authCode = self._getResponse()
            tokenJson = self._getAccessTokenJson(authCode, secret)
            self._saveToken(tokenJson)

    def _genPkceCodeVerifier(self):
        """Generates a secret for use with PKCE verification. See 
        https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
        for more details on use of PKCE authorization with Spotify

        :return: The PKCE code verifier, encoded in base-64
        :rtype: str 
        """
        secret = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8').rstrip('=')
        return secret

    def _genPkceChallenge(self, codeVerifier: str):
        """Generates a challenge for use with PKCE verification. See 
        https://developer.spotify.com/documentation/web-api/tutorials/code-pkce-flow
        for more details on use of PKCE authorization with Spotify
        
        :param codeVerifier: The code verifier to use with the PKCE algorithm
        :type codeVerifier: String
        :return: A string of the hased code verifier, encoded in base-64 
        :rtype: str 
        """
        hash = hashlib.sha256(codeVerifier.encode('utf-8')).digest()
        hashEncoded = base64.urlsafe_b64encode(hash).decode('utf-8').rstrip('=')
        return hashEncoded

    def _getAuthorizationUrl(self, challenge: str):
        """Generates the URL needed in order to request an Authorization token from Spotify.
        
        :param challenge: the PKCE challenge for the authorization to take place
        :type challenge: String
        :return: The Spotify authorization URL 
        :rtyle: String
        """
        authUrl = (
            f"https://accounts.spotify.com/authorize"
            f"?client_id={self.clientId}"
            f"&response_type=code"
            f"&redirect_uri={REDIRECT_URI}"
            f"&code_challenge_method=S256"
            f"&code_challenge={challenge}"
            f"&scope=user-read-playback-state user-modify-playback-state"
            )
        return authUrl

    def _getResponse(self):
        """Handle the callback from the Spotify web browser login session. This method
        receives the authentication code from Spotify via HTTP, and returns it
        
        :return: The Spotify authentication code
        :rtype: str 
        """
        authCode = []

        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urlparse.urlparse(self.path)
                query = urlparse.parse_qs(parsed.query)

                if 'code' in query:
                    authCode.append(query['code'][0])
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b"Authorization complete. You can now close this window :)")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Authorization failed :/")

            # Overwrite log_message of BaseHTTPRequestHandler to prevent printing to console
            def log_message(self, format, *args):
                pass

        serverAddr = ('', 8888)
        httpd = HTTPServer(serverAddr, RequestHandler)
        httpd.handle_request()
        return authCode[0]

    def _getAccessTokenJson(self, code: str, codeVerifier: str):
        """Requests the access token from the Spotify API and returns it.

        :param code: The PKCE code to send to Spotify 
        :type code: String
        :param codeVerifier: The PKCE code verifier to send to Spotify
        :type codeVerifier: String
        :return: The JSON data for the access token
        :rtype: dict 
        """

        tokenUrl = 'https://accounts.spotify.com/api/token' 

        response = requests.post(tokenUrl, data={
            'client_id': self.clientId,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI,
            'code_verifier': codeVerifier
            })

        if response.status_code == 200:
            tokenData = response.json()
            return tokenData 
        else:
            raise Exception("Unable to convert auth code into access token - Response:", response.status_code)
        
    def _refreshAccessToken(self):
        """ Refreshes the Spotify API access token using a stored refresh token. If no
        refresh token is found stored in .env, requestAuth() is called instead """
        if not self.tokenExpired:
            return

        refreshToken = get_key(envPath, 'TFY_REFRESH_TOKEN')

        if refreshToken == None:
            self.requestAuth()
            return

        url = 'https://accounts.spotify.com/api/token'
        response = requests.post(url, data={
            'grant_type': 'refresh_token',
            'refresh_token': refreshToken,
            'client_id': self.clientId 
            })

        self._saveToken(response.json())

    def _saveToken(self, tokenJson):
        """Saves the Spotify API access token to a .env file in the user specified 
        envPath.
        """
        token = tokenJson.get('access_token')
        refreshToken = tokenJson.get('refresh_token')
        
        lifetime = int(tokenJson.get('expires_in'))
        currentTime = int(time())

        expirationTime = currentTime + lifetime

        set_key(envPath, "TFY_ACCESS_TOKEN", str(token))
        set_key(envPath, "TFY_REFRESH_TOKEN", str(refreshToken))
        set_key(envPath, "TFY_TOKEN_EXPIRATION", str(expirationTime))
    
    def tokenExpired(self):
        """Check whether the Spotify API access token has expired and needs to be refresh.
        :return: True if token is expired, False if not
        :rtype: bool 
        """
        try:
           expirationTime = get_key(envPath, 'TFY_TOKEN_EXPIRATION')
           assert(expirationTime != None)
           expirationTime = int(expirationTime)
           currentTime = int(time())
           return currentTime >= expirationTime
        except Exception as e:
            return True


    def getToken(self):
        """Get the current API access token
        :return: Spotify API access token
        :rtype: str
        """
        return get_key(envPath, 'TFY_ACCESS_TOKEN')

