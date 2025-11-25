import os, json, time, requests
from _helpers import get_spotify_access_token

def main():
    if not os.path.exists('output/playlist_data.json'):
        print('playlist_data.json missing; run fetch_playlist.py first')
        return
    with open('output/playlist_data.json','r',encoding='utf-8') as f:
        pd = json.load(f)
    token, method = get_spotify_access_token()
    if not token:
        print('No token available for audio-analysis request; set SPOTIFY_REFRESH_TOKEN or client credentials.')
        return
    headers = {'Authorization': f'Bearer {token}'}
    analyses = {}
    for it in pd.get('items',[]):
        t = it.get('track') or {}
        tid = t.get('id')
        if not tid: continue
        r = requests.get(f'https://api.spotify.com/v1/audio-analysis/{tid}', headers=headers, timeout=30)
        if r.status_code==200:
            analyses[tid] = r.json()
        else:
            analyses[tid] = {'error': r.text, 'status': r.status_code}
            if r.status_code==403:
                print('403 on audio-analysis for', tid)
        time.sleep(0.12)
    os.makedirs('output', exist_ok=True)
    with open('output/audio_analysis.json','w',encoding='utf-8') as f:
        json.dump(analyses,f,indent=2)
    print('Saved output/audio_analysis.json')

if __name__ == '__main__':
    main()
