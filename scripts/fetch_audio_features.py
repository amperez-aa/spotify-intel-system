import os, json, requests, time
def get_token():
    import base64, requests
    CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
    CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
    b64 = __import__('base64').b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    r = requests.post('https://accounts.spotify.com/api/token', data={'grant_type':'client_credentials'}, headers={'Authorization':f'Basic {b64}'})
    r.raise_for_status()
    return r.json()['access_token']

with open('output/playlist_data.json') as f:
    playlist = json.load(f)

track_ids = []
for it in playlist.get('items',[]):
    t = it.get('track') or {}
    if t.get('id'):
        track_ids.append(t['id'])

token = get_token()
headers = {'Authorization':f'Bearer {token}'}

features = {}
for i in range(0, len(track_ids), 100):
    chunk = track_ids[i:i+100]
    ids = ','.join(chunk)
    r = requests.get(f'https://api.spotify.com/v1/audio-features?ids={ids}', headers=headers)
    if r.status_code==200:
        for feat in r.json().get('audio_features',[]):
            if feat:
                features[feat['id']] = feat
    else:
        print('audio-features failed', r.status_code, r.text)
    time.sleep(0.1)

os.makedirs('output', exist_ok=True)
with open('output/audio_features.json','w') as f:
    json.dump(features,f,indent=2)
print('Saved output/audio_features.json')
