import json, os
camelot_map = {
    (0,1): '8B', (0,0): '8A', (1,1): '3B', (1,0): '3A', (2,1): '10B', (2,0): '10A',
    (3,1): '5B', (3,0): '5A', (4,1): '12B', (4,0): '12A', (5,1): '7B', (5,0): '7A',
    (6,1): '2B', (6,0): '2A', (7,1): '9B', (7,0): '9A', (8,1): '4B', (8,0): '4A',
    (9,1): '11B', (9,0): '11A', (10,1): '6B', (10,0): '6A', (11,1): '1B', (11,0): '1A'
}

with open('output/audio_features.json') as f:
    feats = json.load(f)

harmonic = {}
for tid, v in feats.items():
    try:
        key = int(v.get('key', 0))
        mode = int(v.get('mode', 0))
        camelot = camelot_map.get((key,mode),'unknown')
        harmonic[tid] = {'key': key, 'mode': mode, 'camelot': camelot, 'energy': v.get('energy')}
    except Exception as e:
        harmonic[tid] = {'error': str(e)}

os.makedirs('output', exist_ok=True)
with open('output/harmonic_path.json','w') as f:
    json.dump(harmonic, f, indent=2)
print('Saved output/harmonic_path.json')
