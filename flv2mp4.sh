#!/bin/bash

# annie convert and sort

flv_search_convert() {
	IFS=$(echo -en "\n\b")

	for element in `ls "${1}"`; do
		# echo "Cur Element: ${element}"
		dir_or_file="${1}/${element}"

		if [ -d "${dir_or_file}" ]; then	
			echo " --- DIR ${dir_or_file} ---"
			flv_search_convert "${dir_or_file}" "${2}"
		
		elif [ -f "${dir_or_file}" ]; then
			echo " --- FILE ${dir_or_file} ---"
			suffix="${dir_or_file##*.}"
			
			if [ ${suffix} = "flv" ]; then
				
				output=$(basename "$dir_or_file" .flv).mp4
				dirname=$(dirname "$dir_or_file")
				echo "	outputname: ${output}"
				echo "	dirname: ${dirname}"

				ffmpeg -i "${dirname}/${element}" -c copy -movflags +faststart -y "${dirname}/$(basename "$element" .flv).mp4"
				
				if [[ ${2} = "N" || ${2} = "n" ]]; then
					rm "${dirname}/${element}"
				fi

			fi
		fi
	done	
}

main() {

	read -p "Keep original flv files? (Y/N) " keep_flv
	flv_search_convert "." "${keep_flv}"
}

main

