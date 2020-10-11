#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_DIR="${CURRENT_DIR}/.."
BASE_DIR="${APP_DIR}/.."

AVAILABLE_FILE=(taipei_passerby_buying_power.ipynb taipei_passerby_prediction.ipynb taipei_restaurant_distribution.ipynb taipei_shop_rent_cost.ipynb)

for file in ${AVAILABLE_FILE[@]}; do
    path="$CURRENT_DIR/../$file"
    [[ ! -f $path ]] && echo "ERROR: file in $path not found" && exit
    echo "INFO: will process $path"
    $CURRENT_DIR/export_pdf.sh $path $BASE_DIR/analysis/
done
