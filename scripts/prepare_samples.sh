#!/bin/bash
# Download environmental sound samples from Wikimedia Commons and convert to 48kHz stereo wav.
# Requires: curl, ffmpeg
set -euo pipefail
cd "$(dirname "$0")/../samples"

declare -a urls=(
  "https://upload.wikimedia.org/wikipedia/commons/4/42/Rain_and_thunder.ogg|rain"
  "https://upload.wikimedia.org/wikipedia/commons/f/f1/Oceanwavescrushing.ogg|ocean"
  "https://upload.wikimedia.org/wikipedia/commons/d/d3/TTC_Subway_Line_1_Ambience_-_Museum_to_Union_%28Freesound%29.ogg|subway"
  "https://upload.wikimedia.org/wikipedia/commons/e/e6/WWS_TheStationTunnelOfTheTampereStation.ogg|station"
  "https://upload.wikimedia.org/wikipedia/commons/c/c8/Great_Blue_Turaco_%28Corythaeola_cristata%29_%28022A-WA03044X0043-0035M0%29.ogg|birds"
)

for entry in "${urls[@]}"; do
  url="${entry%%|*}"; name="${entry##*|}"
  ogg="${name}.ogg"
  [ -f "$ogg" ] || curl -sL -o "$ogg" "$url"
  ffmpeg -v error -y -i "$ogg" -ac 2 -ar 48000 "${name}.wav"
  echo "ok: ${name}.wav"
done
