# Spotify Intelligence & Mix Automation — Full System

This repository automates fetching Spotify playlist data and produces a DJ-grade intelligence pack:
- playlist metadata (paginated)
- audio-features (tempo, energy, danceability, etc.)
- audio-analysis (beats, bars, segments)
- waveform generation (proxy and full)
- harmonic intelligence (Camelot)
- clustering, optimal ordering
- beatgrid & suggested cut points
- AI mix timeline with overlap logic
- printable PDF mix blueprint
- optional snapshot PR creation
- devcontainer for Codespaces

## Quick install (upload files + add secrets)
1. Create a new GitHub repo.
2. Upload all files and folders from this project.
3. Add GitHub repo secrets:
   - SPOTIFY_CLIENT_ID
   - SPOTIFY_CLIENT_SECRET
   - (optional) GITHUB_PAT — for snapshot PR creation (repo scope)
4. Go to Actions → Spotify Full Intelligence Pipeline → Run workflow

## Where to find outputs
Open the repository → `output/` after the run completes:
- playlist_data.json
- audio_features.json
- audio_analysis.json
- waveforms/<track_id>.png
- harmonic_path.json
- clusters.json
- optimal_order.json
- cuts.json
- ai_mix_timeline.json
- mix_blueprint.pdf

## Run locally (optional)
1. Clone repo
2. python3 -m venv venv && source venv/bin/activate
3. pip install -r requirements.txt
4. export SPOTIFY_CLIENT_ID=...
   export SPOTIFY_CLIENT_SECRET=...
5. Run scripts in order:
   python scripts/fetch_playlist.py
   python scripts/fetch_audio_features.py
   python scripts/fetch_audio_analysis.py
   python scripts/waveform_generator.py
   python scripts/harmonic_engine.py
   python scripts/cluster_tracks.py
   python scripts/optimal_order.py
   python scripts/beatgrid_and_cuts.py
   python scripts/ai_mix_timeline.py
   python scripts/mix_blueprint_pdf.py

## Notes
- Uses Spotify Client Credentials (public playlists).
- Audio-analysis sometimes unavailable for certain tracks; errors captured.
- Waveform generator produces proxy images when full audio is not provided.
- Tweak heuristics in scripts/ to fit your mixing preferences.
