import os, json, time, requests
from _helpers import get_spotify_access_token

def main():
    if not os.path.exists('output/playlist_data.json'):
        print('playlist_data.json missing; run fetch_playlist.py first')
        return
    with open('output/playlist_data.json','r',encoding='utf-8') as f:
        pd = json.load(f)
    track_ids = []
    for it in pd.get('items',[]):
        t = it.get('track') or {}
        if t.get('id'):
            track_ids.append(t['id'])

    token, method = get_spotify_access_token()
    if not token:
        print('No token available for audio-features request; set SPOTIFY_REFRESH_TOKEN or client credentials.')
        return

    headers = {'Authorization': f'Bearer {token}'}
    features = {}
    for i in range(0, len(track_ids), 100):
        chunk = track_ids[i:i+100]
        ids = ','.join(chunk)
        r = requests.get(f'https://api.spotify.com/v1/audio-features?ids={ids}', headers=headers, timeout=30)
        if r.status_code == 200:
            for feat in r.json().get('audio_features',[]):
                if feat:
                    features[feat['id']] = feat
        else:
            print('audio-features failed', r.status_code, r.text)
            if r.status_code == 403:
                print('403 received. This often means you need a user access token with playlist scopes (use Authorization Code Flow and save SPOTIFY_REFRESH_TOKEN).')
        time.sleep(0.12)

    os.makedirs('output', exist_ok=True)
    with open('output/audio_features.json','w',encoding='utf-8') as f:
        json.dump(features, f, indent=2)
    print('Saved output/audio_features.json')

if __name__ == '__main__':
    main()
