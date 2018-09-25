#!/bin/bash

PY3=`command -v python3-coverage`
COV=`command -v coverage`

if [[ "$PY3" != "" ]]; then
	CMD=python3-coverage
elif [[ "$COV" != "" ]]; then
	CMD=coverage
else
	echo "Coverage command not found. Try: pip3 install coverage"
	exit 1
fi

$CMD run -m unittest
$CMD html
nohup python3 -m webbrowser htmlcov/index.html > /dev/null 2>&1
