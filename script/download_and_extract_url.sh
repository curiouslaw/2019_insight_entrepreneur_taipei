#!/bin/bash

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
AVAILABLE_ARGUMENTS=(taipei_mrt_info taipei_travel_network)

# extract compressed file in a directory and delete the original file
extract_compressed_in_dir() {
	local arg_output_dir=$1
	echo "arg_output_dir = $arg_output_dir"
	echo "arg = $1"

	for filepath in $(find $arg_output_dir -name '*.tar.gz' | sed 's@//@/@'); do	
		echo "INFO: extracting ${filepath}"
		
		tar -xf $filepath -C $arg_output_dir
		if [ $? -eq 0 ]; then
			echo "INFO: clean compressed file in $filepath"
			[[ -f $filepath ]] && rm $filepath
		else
			echo "ERROR: fail extract $filepath"
			exit
		fi
	done

	for filepath in $(find $arg_output_dir -name '*.gz' ! -name "*.tar.gz" | sed 's@//@/@'); do	
		echo "INFO: extracting ${filepath}"
		
		gzip -d $filepath
		if [ $? -eq 0 ]; then
			echo "INFO: clean compressed file in $filepath"
			[[ -f $filepath ]] && rm $filepath
		else
			echo "ERROR: fail extract $filepath"
			exit
		fi
	done

	for filepath in $(find $arg_output_dir -name '*.7z' | sed 's@//@/@'); do	
		echo "INFO: extracting ${filepath}"
		
		7za x $filepath -o $arg_output_dir
		if [ $? -eq 0 ]; then
			echo "INFO: clean compressed file in $filepath"
			rm $filepath
		else
			echo "ERROR: fail extract $filepath"
			exit
		fi
	done

}

print_availabe_argument() {
    echo -e "available $1:"
	for data_name in ${AVAILABLE_ARGUMENTS[@]}; do
		echo -e "  $data_name"
	done
}

# start of the main function / script

if [[ $# -eq 0 ]]; then
  	echo -e "usage:\t$(basename $0) [data name]"
	print_availabe_argument "[data_name]"

elif [[ $1 == '-h' ]]; then
	echo -e "this bash script will download and extract un-attached data from listed url. For usage information, run the script without any argument."

else
	for arg in ${AVAILABLE_ARGUMENTS[@]}; do
		if [[ $arg == $1 ]]; then
			url_path="$CURRENT_DIR/../data/$1/download_links.txt"
			output_dir="$CURRENT_DIR/../data/$1/download/"

			[[ ! -f $url_path ]] && echo "ERROR: links file $url_path not found" && exit

			echo "INFO: will reading link list in $url_path"
			echo "INFO: begin downloading file to $output_dir"

			wget -i $url_path --content-disposition -P $output_dir

			echo "INFO: file download finished"
			echo "INFO: begin extracting file"
			
			extract_compressed_in_dir $output_dir
			
			echo "INFO: file extraction complete"
			exit 0
		fi		
	done

	echo "ERROR: argument not recognized"
	print_availabe_argument argument
	exit
fi

