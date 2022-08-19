# define the name of the virtual environment directory
VENV := venv

install: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip install -r requirements.txt

run: install
	./$(VENV)/bin/flask run

clean:
	rm -rf $(VENV)
	find . -type f -name '*.pyc' -delete

.PHONY: all install run clean