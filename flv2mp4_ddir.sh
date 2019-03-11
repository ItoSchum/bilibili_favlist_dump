#!/bin/zsh

# annie convert and sort

for j in `ls .`; do
	
	for i in "$j"/*.flv; do
		
		output=$(basename "$i" .flv).mp4
		dirname=$(dirname "$i")
		echo "$output"
		echo "$dirname"

		ffmpeg -i "$i" -c copy -movflags +faststart "$(basename $i .flv).mp4"
		
		mv "$(basename $i .flv).mp4" "$dirname"
		mv "$(basename $i .flv).xml" "$dirname"

		rm "$i"
	done

done
