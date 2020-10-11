#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_DIR="${CURRENT_DIR}/.."
BASE_DIR="${APP_DIR}"

$CURRENT_DIR/export_slides.sh ${BASE_DIR}/presentation.ipynb $BASE_DIR/
