#!/bin/zsh

# annie convert and sort

for i in ./*.flv; do
	
	ffmpeg -i "$i" -c copy -movflags +faststart "$(basename $i .flv).mp4"

	dirname=~/Movies/Bilibili/"$(basename $i .flv)"
	
	mkdir "$dirname"
	mv "$(basename $i .flv).mp4" "$dirname"
	mv "$(basename $i .flv).xml" "$dirname"

	rm "$i"
done
