#!/usr/bin/env bash
echo $BASH_VERSION

CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
APP_DIR="${CURRENT_DIR}/.."
TEMPLATE="custom_hide_code_slides.tpl"


export_func() {
    local input_filepath=$1
    local output_dirpath=$2

    cp ${APP_DIR}/src/${TEMPLATE} ./.${TEMPLATE}
    jupyter nbconvert --to hide_code_slides ${input_filepath} \
        --execute --ExecutePreprocessor.timeout=-1 --no-prompt \
        --template .${TEMPLATE} \
        --output-dir ${output_dirpath}
        
    if [[ -f .${TEMPLATE} ]]; then
        rm .${TEMPLATE}
    fi
}

if [[ $# -eq 0 ]]; then
  	echo -e "usage:\t$(basename $0) [input filepath] [output dir]"

elif [[ $# -ne 2 ]]; then
    echo -e "please input 2 argument"
    echo -e "usage:\t$(basename $0) [input filepath] [output dir]"
else
    export_func $1 $2
fi
