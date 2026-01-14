#!/bin/bash

# Ensure we are in the script's directory
cd "$(dirname "$0")"

# Kill any existing python server on port 8085 to avoid conflicts (optional but safer)
fuser -k 8085/tcp > /dev/null 2>&1

echo "Starting BiteBabe Website Server..."
# Start Python HTTP server in background
python3 -m http.server 8085 &
SERVER_PID=$!

# Wait a moment for server to start
sleep 2

# Open in default browser
echo "Opening http://localhost:8085 ..."
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:8085
elif command -v python3 > /dev/null; then
    python3 -m webbrowser http://localhost:8085
else
    echo "Could not detect browser opener. Please open http://localhost:8085 manually."
fi

# Keep script running to keep server alive
echo "Server is running (PID: $SERVER_PID)"
echo "Press Ctrl+C to stop the server."
wait $SERVER_PID
