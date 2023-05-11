#!/bin/bash

contentdir="../content"
staticdir="../static"
templatedir="../templates"

cleanup() {
    echo "Stopping the server..."
    kill $(pgrep -f "python -m http.server")
    exit
}
trap cleanup SIGINT

python generate.py
cd build/
python -m http.server &
inotifywait -r -m -e modify "${contentdir}" "${staticdir}" "${templatedir}" |
while read -r directory event file; do
    echo "File '${file}' modified in '${directory}'"
    kill $(pgrep -f "python -m http.server")
    cd ..
    python generate.py
    cd build/
    python -m http.server &
done
