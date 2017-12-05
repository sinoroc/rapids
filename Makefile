#


toxenvname ?= unknown


source_dir := ./src
tests_dir := ./tests


.DEFAULT_GOAL := develop


.PHONY: nothing
nothing:
	true


.PHONY: develop
develop:
	python setup.py develop


.PHONY: install
install:
	python setup.py install


.PHONY: package
package: sdist wheel


.PHONY: sdist
sdist:
	python setup.py sdist


.PHONY: wheel
wheel:
	python setup.py bdist_wheel


.PHONY: check
check:
	python setup.py check --metadata --restructuredtext --strict


.PHONY: lint
lint:
	pytest --pep8 --pylint -m 'pep8 or pylint'


.PHONY: pep8
pep8:
	pytest --pep8 -m pep8


.PHONY: pylint
pylint:
	pytest --pylint -m pylint


.PHONY: test
test: pytest


.PHONY: pytest
pytest:
	pytest


.PHONY: review
review: check
	pytest --pep8 --pylint


.PHONY: clean
clean:
	$(RM) --recursive ./.cache/
	$(RM) --recursive ./.eggs/
	$(RM) --recursive ./build/
	$(RM) --recursive ./dist/
	$(RM) --recursive ./__pycache__/
	find $(source_dir) -name '*.dist-info' -type d -exec $(RM) --recursive {} +
	find $(source_dir) -name '*.egg-info' -type d -exec $(RM) --recursive {} +
	find $(source_dir) -name '*.pyc' -type f -exec $(RM) {} +
	find $(tests_dir) -name '*.pyc' -type f -exec $(RM) {} +
	find $(source_dir) -name '__pycache__' -type d -exec $(RM) --recursive {} +
	find $(tests_dir) -name '__pycache__' -type d -exec $(RM) --recursive {} +


#
# Options
#

# Disable default rules and suffixes (improve speed and avoid unexpected behaviour)
MAKEFLAGS := --no-builtin-rules
.SUFFIXES:


# EOF
