PYTHON = python

TEST_RUNNER = unittest
TEST_ARGS = discover -v

MANAGE_SCRIPT = manage.py

DB_USER = root
DB_PASS = 1234
DB_NAME = curpub

run:
	$(PYTHON) $(MANAGE_SCRIPT) run

install:
	pip install -r requeriments.txt
	mysql -u $(DB_USER) -p$(DB_PASS) -e "create database IF NOT EXISTS $(DB_USER);"

test:
	$(PYTHON) -m $(TEST_RUNNER) $(TEST_RUNNER_ARGS)
