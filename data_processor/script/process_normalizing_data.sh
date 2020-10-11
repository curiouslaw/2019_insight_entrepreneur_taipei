#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_DIR="${CURRENT_DIR}/.."

AVAILABLE_DATA=(taipei_income_by_village taipei_mrt_info_data taipei_shop_rent_price_data)

for filename in ${AVAILABLE_DATA[@]}; do
    filepath=$APP_DIR/normalize_$filename.py
    echo "INFO: will process $filepath"
    python $filepath
done