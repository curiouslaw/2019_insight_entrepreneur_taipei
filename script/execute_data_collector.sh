#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${CURRENT_DIR}/.."
DATA_COLLECTOR_DIR="${BASE_DIR}/data_collector"

${DATA_COLLECTOR_DIR}/script/process_download_data.sh
${DATA_COLLECTOR_DIR}/script/process_scrape_metro_data.sh
${DATA_COLLECTOR_DIR}/script/process_scrape_591_data.sh
