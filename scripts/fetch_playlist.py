import os, base64, requests, json, time

CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
PLAYLIST_ID = '5Dn46HjcxZj5XDTGvNP8gH'  # update if needed

def get_token():
    auth = f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    import base64
    b64 = base64.b64encode(auth).decode()
    r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'client_credentials'}, headers={'Authorization':f'Basic {b64}'})
    r.raise_for_status()
    return r.json()['access_token']

def fetch_all_tracks(token):
    headers = {'Authorization':f'Bearer {token}'}
    url = f'https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks'
    params = {'limit':100, 'offset':0}
    items = []
    while True:
        r = requests.get(url, headers=headers, params=params)
        if r.status_code != 200:
            print('Failed to fetch playlist:', r.status_code, r.text)
            break
        d = r.json()
        items.extend(d.get('items',[]))
        if d.get('next'):
            params['offset'] += params['limit']
            time.sleep(0.1)
        else:
            break
    return items

def main():
    token = get_token()
    items = fetch_all_tracks(token)
    out = {'playlist_id': PLAYLIST_ID, 'items': items}
    os.makedirs('output', exist_ok=True)
    with open('output/playlist_data.json', 'w') as f:
        json.dump(out, f, indent=2)
    print('Saved output/playlist_data.json')

if __name__ == '__main__':
    main()
