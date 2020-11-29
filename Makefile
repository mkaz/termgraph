# Makefile for termgraph

.PHONY: clean
clean:
	rm -rf dist/*

# Requirement
# python3 -m pip install wheel
.PHONY: build
build: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel


# Publish
# Requires: python3 -m pip install twine
.PHONY: publish
publish: build
	twine upload dist/*

# Test
# Requires: python3 -m pip install pytest pytest-sugar
.PHONY: test
test:
	py.test tests/
