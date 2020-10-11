#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_DIR="${CURRENT_DIR}/.."
BASE_DIR="${APP_DIR}/.."

MAIN_DATA_FILEPATH="$BASE_DIR/data/taipei_shop_rent_price/download-data_lake/591_xhr_responses.json"
LAT_LONG_DATA_FILEPATH="$BASE_DIR/data/taipei_shop_rent_price/download-data_lake/591_lat_long_lookup.json"


# if file not exist, try to download, if exist use before
if [[ ! -f ${MAIN_DATA_FILEPATH} ]]; then
    python ${APP_DIR}/scrape_taipei_shop_rent_price_main_data.py
fi

# continue form previous data scrapping
resume_previous=$(wc -l < ${LAT_LONG_DATA_FILEPATH} | awk '{print $1}')
resume_previous=$(( $resume_previous + 1 ))
python ${APP_DIR}/scrape_taipei_shop_rent_price_long_lat_data.py -s ${resume_previous}
