import os, requests

def get_spotify_access_token():
    """
    Returns (access_token, method)
    method: 'refresh' if refresh-token was used, 'client_credentials' otherwise, or (None, None).
    Requires SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET; for user-token workflow also SPOTIFY_REFRESH_TOKEN.
    """
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')

    # Try refresh-token exchange first (user-level access — can access private playlists)
    if refresh_token and client_id and client_secret:
        url = 'https://accounts.spotify.com/api/token'
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret
        }
        try:
            r = requests.post(url, data=data, timeout=30)
            r.raise_for_status()
            j = r.json()
            token = j.get('access_token')
            if token:
                return token, 'refresh'
        except Exception as e:
            print('Refresh-token exchange failed:', e)

    # Fallback: Client Credentials (only for public data)
    if client_id and client_secret:
        import base64
        b64 = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        try:
            r = requests.post('https://accounts.spotify.com/api/token',
                              data={'grant_type':'client_credentials'},
                              headers={'Authorization':f'Basic {b64}'}, timeout=30)
            r.raise_for_status()
            return r.json().get('access_token'), 'client_credentials'
        except Exception as e:
            print('Client credentials token failed:', e)

    return None, None
