#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

${CURRENT_DIR}/execute_data_collector.sh
${CURRENT_DIR}/execute_data_processor.sh
${CURRENT_DIR}/execute_data_analysis.sh
${CURRENT_DIR}/publish_slides.sh
