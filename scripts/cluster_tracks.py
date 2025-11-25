import json, os
from sklearn.cluster import KMeans
import numpy as np

with open('output/audio_features.json') as f:
    feats = json.load(f)

ids=[]
rows=[]
for tid,v in feats.items():
    if v is None: continue
    ids.append(tid)
    rows.append([v.get('tempo',0), v.get('energy',0), v.get('danceability',0), v.get('valence',0)])

if not rows:
    print('No features to cluster.')
    with open('output/clusters.json','w') as f:
        json.dump({'clusters':{}}, f)
    exit(0)

X = np.array(rows)
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
Xs = sc.fit_transform(X)
k = min(6, max(2, len(ids)//5))
km = KMeans(n_clusters=k, random_state=0).fit(Xs)
labels = km.labels_.tolist()
clusters={}
for tid,label in zip(ids, labels):
    clusters.setdefault(str(label), []).append(tid)

os.makedirs('output', exist_ok=True)
with open('output/clusters.json','w') as f:
    json.dump({'clusters':clusters,'k':k}, f, indent=2)
print('Saved output/clusters.json')
