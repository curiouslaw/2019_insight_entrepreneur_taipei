#!/usr/bin/env bash

jupyter nbconvert --to hide_code_slides recommendation_reveal_js.ipynb --template custom_hide_code_slides.tpl --execute --ExecutePreprocessor.timeout=-1 --no-prompt
