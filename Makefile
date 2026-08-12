.PHONY: run test

run:
	python -m scrum_health.server

test:
	python -m unittest discover -s tests -v

