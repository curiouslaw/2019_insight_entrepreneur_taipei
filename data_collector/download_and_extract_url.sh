#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
AVAILABLE_ARGUMENTS=(taipei_mrt_info taipei_map_points taipei_travel_network taiwan_twd97_map_data_county taiwan_twd97_map_data_township taiwan_twd97_map_data_village)

# extract compressed file in a directory and delete the original file
extract_compressed_in_dir() {
	local arg_output_dir=$1

	for filepath in $(find $arg_output_dir -name '*.tar.gz' | sed 's@//@/@'); do	
		echo "INFO: extracting ${filepath}"
		
		tar -xf $filepath -C $arg_output_dir
		if [ $? -eq 0 ]; then
			echo "INFO: clean compressed file in $filepath"
			[[ -f $filepath ]] && rm $filepath
		else
			echo "ERROR: fail extract $filepath"
			exit 45
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
			exit 45
		fi
	done

	for filepath in $(find $arg_output_dir -name '*.zip' | sed 's@//@/@'); do	
		echo "INFO: extracting ${filepath}"
		
		tar -xf $filepath -C $arg_output_dir
		if [ $? -eq 0 ]; then
			echo "INFO: clean compressed file in $filepath"
			[[ -f $filepath ]] && rm $filepath
		else
			echo "ERROR: fail extract $filepath"
			exit 45
		fi
	done

	for filepath in $(find $arg_output_dir -name '*.7z' | sed 's@//@/@'); do	
		echo "INFO: extracting ${filepath}"
		
		7za x $filepath -o$arg_output_dir
		if [ $? -eq 0 ]; then
			echo "INFO: clean compressed file in $filepath"
			rm $filepath
		else
			echo "ERROR: fail extract $filepath"
			exit 45
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
	echo -e "This bash script will download and extract un-attached data from listed url."
	echo -e "WARNING: this bash script will firstly clean the download folder after succesfully reading links, use with caution.\n"
	echo -e "usage:\t$(basename $0) [data name]"
	print_availabe_argument "[data_name]"	

else
	for arg in ${AVAILABLE_ARGUMENTS[@]}; do
		if [[ $arg == $1 ]]; then
			url_path="$CURRENT_DIR/../data/$1/download_links.txt"
			output_dir="$CURRENT_DIR/../data/$1/download-data_lake/"

			[[ ! -f $url_path ]] && echo "ERROR: links file $url_path not found" && exit

			echo "INFO: will reading link list in $url_path"
			echo "INFO: will clean the download folder $output_dir"
			rm -rf $output_dir*

			echo "INFO: begin downloading file to $output_dir"

			wget -i $url_path --content-disposition -P $output_dir
			if [[ $? -ne 0 ]]; then
				wget -i $url_path -P $output_dir
				if [[ $? -ne 0 ]]; then
					echo "ERROR: error on downloading links"
					exit
				fi
			fi

			echo "INFO: file download finished"
			echo "INFO: trying extracting file if it compressed file"
			
			extract_compressed_in_dir $output_dir
			
			echo "INFO: finish job"
			exit 0
		fi		
	done

	echo "ERROR: argument not recognized"
	print_availabe_argument argument
	exit 45
fi
