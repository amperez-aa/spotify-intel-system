import os, json, time, requests
from _helpers import get_spotify_access_token

PLAYLIST_ID = os.getenv('PLAYLIST_ID', '5Dn46HjcxZj5XDTGvNP8gH')

def fetch_all_tracks(token):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks'
    params = {'limit':100, 'offset':0}
    items = []
    while True:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        if r.status_code == 200:
            d = r.json()
            items.extend(d.get('items', []))
            if d.get('next'):
                params['offset'] += params['limit']
                time.sleep(0.1)
                continue
            break
        else:
            print('Failed to fetch playlist', r.status_code, r.text)
            break
    return items

def main():
    token, method = get_spotify_access_token()
    if not token:
        print('No Spotify token available. Set SPOTIFY_REFRESH_TOKEN or SPOTIFY_CLIENT_ID/SECRET.')
        return
    items = fetch_all_tracks(token)
    out = {'playlist_id': PLAYLIST_ID, 'items': items, 'auth_method': method}
    os.makedirs('output', exist_ok=True)
    with open('output/playlist_data.json', 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=2)
    print('Saved output/playlist_data.json')

if __name__ == '__main__':
    main()
