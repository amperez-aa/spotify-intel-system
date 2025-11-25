import json, os
with open('output/audio_analysis.json') as f:
    analyses = json.load(f)

cuts={}
for tid, a in analyses.items():
    if isinstance(a, dict) and 'beats' in a and a['beats']:
        beats = a['beats']  # list of [time, duration]
        entry = beats[0][0] if beats else 0
        cut_idx = min(31, len(beats)-1)
        cut = beats[cut_idx][0] if len(beats)>1 else None
        cuts[tid] = {'entry_s': entry, 'cut32_s': cut, 'num_beats': len(beats)}
    else:
        cuts[tid] = {'error': 'no beats'}

os.makedirs('output', exist_ok=True)
with open('output/cuts.json','w') as f:
    json.dump(cuts, f, indent=2)
print('Saved output/cuts.json')
