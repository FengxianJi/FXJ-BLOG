PYTHON ?= python3

.PHONY: check figures sync
check:
	$(PYTHON) scripts/manage_blog.py check
figures:
	$(PYTHON) scripts/manage_blog.py figures
sync:
	$(PYTHON) scripts/manage_blog.py sync
