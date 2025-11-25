import json, os
with open('output/optimal_order.json') as f:
    order = json.load(f).get('ordered_tracks',[])
cuts={}
if os.path.exists('output/cuts.json'):
    with open('output/cuts.json') as f:
        cuts = json.load(f)

timeline=[]
cursor=0.0
for t in order:
    tid=t['id']
    dur=180.0
    # get real duration
    if os.path.exists('output/playlist_data.json'):
        with open('output/playlist_data.json') as f:
            pd=json.load(f)
        for it in pd.get('items',[]):
            tr=it.get('track') or {}
            if tr.get('id')==tid:
                dur = tr.get('duration_ms',180000)/1000.0
                break
    cut = cuts.get(tid,{})
    start_offset = cut.get('entry_s',0)
    timeline.append({'track_id':tid,'name':t.get('name'),'artists':t.get('artists'),'start_time_s':cursor,'start_offset_s':start_offset,'planned_play_duration_s':min(180,dur)})
    cursor += min(180,dur) - 6

os.makedirs('output', exist_ok=True)
with open('output/ai_mix_timeline.json','w') as f:
    json.dump(timeline,f,indent=2)
print('Saved output/ai_mix_timeline.json')
