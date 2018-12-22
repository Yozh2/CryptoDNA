.PHONY: remake

PACKAGENAME = crypto_dna

all: ui

ui:
	python setup.py build_ui

run:
	python -m $(PACKAGENAME)


remake: all run