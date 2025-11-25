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

token = get_token()
headers = {'Authorization':f'Bearer {token}'}

analyses = {}
for it in playlist.get('items',[]):
    t = it.get('track') or {}
    tid = t.get('id')
    if not tid:
        continue
    r = requests.get(f'https://api.spotify.com/v1/audio-analysis/{tid}', headers=headers)
    if r.status_code==200:
        analyses[tid]=r.json()
    else:
        analyses[tid]={'error':r.text, 'status':r.status_code}
    time.sleep(0.12)

os.makedirs('output', exist_ok=True)
with open('output/audio_analysis.json','w') as f:
    json.dump(analyses,f,indent=2)
print('Saved output/audio_analysis.json')
