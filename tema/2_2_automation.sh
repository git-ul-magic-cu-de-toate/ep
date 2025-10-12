#!/bin/bash

# Set variables
DURATION=60        # Duration in seconds
INTERVAL=1         # Interval in deciseconds (0.1s = 1 decisecond)
OUTPUT_FILE="raw.txt"
COUNTER=0
TOTAL=60        # 60 seconds * 1 samples per second = 60 samples

# Clear the output file if it exists
> "$OUTPUT_FILE"

# Main collection loop
while [ $COUNTER -lt $TOTAL ]; do
    # Run socket_diag command and append output to file
    PID=$(pgrep -f "mininet:h1" 2>/dev/null || pgrep -f "mininet" 2>/dev/null)
    
    if [ -n "$PID" ]; then
        # Process found - run the command
        sudo ./socket_diag /proc/$PID/ns/net >> "$OUTPUT_FILE" 2>&1
    else
        # No process found - log the error
        echo "Error: Could not find Mininet process at sample $COUNTER"
    fi
    
    # Increment counter
    COUNTER=$((COUNTER + 1))
    
    # Sleep for 0.1 seconds
    sleep 1
done

