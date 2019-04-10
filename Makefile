.PHONY: init check test

init:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

check:
	flake8 rainmq --import-order-style=smarkets --max-complexity 12 max-line-length=79
	pylint lv

test:
	make check
	python -m pytest

