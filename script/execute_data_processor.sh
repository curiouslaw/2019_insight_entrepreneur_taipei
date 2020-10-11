#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
BASE_DIR="${CURRENT_DIR}/.."
DATA_PROCESSOR_DIR="${BASE_DIR}/data_processor"

${DATA_PROCESSOR_DIR}/script/process_structuring_data.sh
${DATA_PROCESSOR_DIR}/script/process_normalizing_data.sh
${DATA_PROCESSOR_DIR}/script/process_creating_support_data.sh
