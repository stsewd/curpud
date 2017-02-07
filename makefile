PYTHON = python

TEST_RUNNER = unittest
TEST_ARGS = discover -v

MANAGE_SCRIPT = manage.py

DB_USER = root
DB_PASS = 1234
DB_NAME = curpud

run:
	$(PYTHON) $(MANAGE_SCRIPT) run

install:
	pip install -r requeriments.txt
	mysql -u $(DB_USER) -p$(DB_PASS) -e "create database IF NOT EXISTS $(DB_NAME);"
	mkdir -p instance/files/courses/
	mkdir -p instance/files/publications/
	$(PYTHON) $(MANAGE_SCRIPT) users
	cd curpud/static/ && bower install

test:
	$(PYTHON) -m $(TEST_RUNNER) $(TEST_RUNNER_ARGS)
