mypy mortgage_calculator.py || { echo 'mypy failed' ; exit 1; }
mypy test.py || { echo 'mypy failed' ; exit 1; }

python3 test.py
