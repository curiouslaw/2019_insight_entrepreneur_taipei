#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_DIR="${CURRENT_DIR}/.."

AVAILABLE_DATA=(taipei_mrt_info taipei_travel_network taiwan_twd97_map_data_county taiwan_twd97_map_data_township taiwan_twd97_map_data_village)

for data in ${AVAILABLE_DATA[@]}; do
    echo "INFO: will process $data"
    $APP_DIR/download_and_extract_url.sh $data
done