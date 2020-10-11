#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${CURRENT_DIR}/.."
DATA_ANALYSIS_DIR="${BASE_DIR}/data_analysis"

${DATA_ANALYSIS_DIR}/script/publish_all.sh
