#!/bin/bash

# Start a new tmux session named 'motion_detection'
tmux new-session -d -s motion_detection

# Send commands to the 'motion_detection' session
tmux send-keys -t motion_detection 'cd ~/v2/files/' C-m
tmux send-keys -t motion_detection 'sudo node server.js' C-m
