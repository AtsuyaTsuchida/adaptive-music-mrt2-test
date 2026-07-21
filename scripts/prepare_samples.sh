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
  # long versions (>= 4min, trimmed to 10min max) — for env_mix layers in stream.py
  "https://upload.wikimedia.org/wikipedia/commons/c/cd/Thunderstorm_after_hot_summer_day_17_minutes_01_of_04.ogg|rain_long"
  "https://upload.wikimedia.org/wikipedia/commons/d/de/Dawnchorus-uk.ogg|birds_long"
  "https://upload.wikimedia.org/wikipedia/commons/b/b0/Lake_Okeechobee_Surf_in_April_2016.ogg|ocean_long"
  "https://upload.wikimedia.org/wikipedia/commons/4/4a/Sunday_in_the_center_of_Mexico_City_%28close_to_Alameda_Park%29%2C_Schoeps_MS_Setup.flac|city_long"
)

for entry in "${urls[@]}"; do
  url="${entry%%|*}"; name="${entry##*|}"
  src="${name}.${url##*.}"; src="${src%%\%*}.ogg"; [[ "$url" == *.flac ]] && src="${name}.flac"
  [ -f "$src" ] || curl -sL -A "env-sound-music/1.0" -o "$src" "$url"
  ffmpeg -v error -y -i "$src" -t 600 -ac 2 -ar 48000 "${name}.wav"
  echo "ok: ${name}.wav"
done
