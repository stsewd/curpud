PYTHON = python

TEST_RUNNER = unittest
TEST_ARGS = discover -v

MANAGE_SCRIPT = manage.py

run:
	$(PYTHON) $(MANAGE_SCRIPT) run

install:
	pip install -r requeriments.txt

test:
	$(PYTHON) -m $(TEST_RUNNER) $(TEST_RUNNER_ARGS)
