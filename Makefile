PYTHON ?= python
SRC := src static

clean:
	-rm -rf .pytest_cache

isort:
	find $(SRC) -type f -name "*.py" | xargs isort

check-pylint:
	find $(SRC) -type f -name "*.py" | xargs pylint --rcfile=.pylintrc