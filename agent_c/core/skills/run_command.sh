#!/bin/bash

# Check if enough arguments are provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <terminal_id> <command>"
    exit 1
fi

TERMINAL_ID=$1
COMMAND=$2

# Create a temporary file to store the output
OUTPUT_FILE=$(mktemp)
STATUS_FILE=$(mktemp)

# Run the command in the specified terminal and capture the output
osascript <<EOF
tell application "Terminal"
    do script "$COMMAND > $OUTPUT_FILE 2>&1; echo \$? > $STATUS_FILE" in window id $TERMINAL_ID
end tell
EOF

# Wait for the command to finish
sleep 2

# Read the status from the temporary file
STATUS=$(cat $STATUS_FILE)

# Read the output from the temporary file
OUTPUT=$(cat $OUTPUT_FILE)

# Determine if the command was successful or not
if [ "$STATUS" -eq 0 ]; then
    echo "Command executed successfully"
else
    echo "Command failed with status $STATUS"
fi

# Print the command output
echo "$OUTPUT"

# Remove the temporary files
rm $OUTPUT_FILE
rm $STATUS_FILE
