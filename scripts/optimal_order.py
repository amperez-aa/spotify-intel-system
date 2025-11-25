import json, os
with open('output/playlist_data.json') as f:
    playlist = json.load(f)
with open('output/audio_features.json') as f:
    feats = json.load(f)
clusters = {}
if os.path.exists('output/clusters.json'):
    with open('output/clusters.json') as f:
        clusters = json.load(f).get('clusters',{})

track_map={}
for it in playlist.get('items',[]):
    t = it.get('track') or {}
    if t.get('id'):
        track_map[t['id']] = {'name': t.get('name'), 'artists': [a['name'] for a in t.get('artists',[])]}

cluster_energy={}
for c, ids in clusters.items():
    es=[]
    for tid in ids:
        ff = feats.get(tid)
        if ff: es.append(ff.get('energy',0))
    cluster_energy[c] = sum(es)/len(es) if es else 0

ordered_clusters = sorted(cluster_energy.items(), key=lambda x:x[1])
cluster_order = [c for c,_ in ordered_clusters]

ordered=[]
for c in cluster_order:
    tids = clusters.get(c,[])
    tids_sorted = sorted(tids, key=lambda x: feats.get(x,{}).get('tempo',0))
    for tid in tids_sorted:
        info = track_map.get(tid,{})
        ordered.append({'id':tid,'name':info.get('name'),'artists':info.get('artists'),'tempo':feats.get(tid,{}).get('tempo'),'energy':feats.get(tid,{}).get('energy')})

# Mirror back for arc if multiple clusters
if len(cluster_order)>2:
    for c in reversed(cluster_order[:-1]):
        for tid in clusters.get(c,[]):
            info = track_map.get(tid,{})
            ordered.append({'id':tid,'name':info.get('name'),'artists':info.get('artists'),'tempo':feats.get(tid,{}).get('tempo'),'energy':feats.get(tid,{}).get('energy')})

os.makedirs('output', exist_ok=True)
with open('output/optimal_order.json','w') as f:
    json.dump({'ordered_tracks': ordered}, f, indent=2)
print('Saved output/optimal_order.json')
