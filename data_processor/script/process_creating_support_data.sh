#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_DIR="${CURRENT_DIR}/.."

AVAILABLE_DATA=(chinese_english_column_helper_dictionary goverment_area_categorization simplified_version_of_taipei_map)

for filename in ${AVAILABLE_DATA[@]}; do
    filepath=$APP_DIR/create_$filename.py
    echo "INFO: will process $filepath"
    python $filepath
done