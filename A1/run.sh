#!/bin/bash
now=$(date +%s)
echo $now
python apnasimulator3.py 1 > games_data/$now