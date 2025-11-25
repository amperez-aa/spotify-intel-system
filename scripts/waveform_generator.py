import os, json
# optional heavy libs are imported only if available in runtime
try:
    import librosa, numpy as np, matplotlib.pyplot as plt, soundfile as sf
except Exception:
    librosa = None

os.makedirs('output/waveforms', exist_ok=True)

ana_path = 'output/audio_analysis.json'
if not os.path.exists(ana_path):
    print('audio_analysis not found; waveform generator will produce proxy images based on segments.')
    analyses = {}
else:
    with open(ana_path) as f:
        analyses = json.load(f)

for tid, analysis in analyses.items():
    try:
        segments = analysis.get('segments',[])
        if segments:
            values = [s.get('loudness_max', -60.0) for s in segments]
            import numpy as np, matplotlib.pyplot as plt
            times = list(range(len(values)))
            plt.figure(figsize=(10,2.5))
            plt.plot(times, values)
            plt.title(f'Proxy waveform for {tid}')
            plt.ylabel('loudness_max')
            plt.tight_layout()
            out = f'output/waveforms/{tid}.png'
            plt.savefig(out)
            plt.close()
        else:
            import matplotlib.pyplot as plt
            plt.figure(figsize=(10,2.5))
            plt.text(0.5,0.5,'No segments available',ha='center',va='center')
            plt.axis('off')
            out = f'output/waveforms/{tid}.png'
            plt.savefig(out)
            plt.close()
    except Exception as e:
        print('waveform gen failed for', tid, e)
print('Generated waveform PNGs (proxy).')
