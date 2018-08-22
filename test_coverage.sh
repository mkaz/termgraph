if python3-coverage run -m unittest
then
    python3-coverage html
    nohup python3 -m webbrowser htmlcov/index.html > /dev/null 2>&1
fi
