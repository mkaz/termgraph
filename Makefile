# Makefile for termgraph

.PHONY: clean
clean:
	rm -rf dist/*

.PHONY: build
build: clean
	python3 setup.py sdist
	python3 setup.py bdist_wheel

