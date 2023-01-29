PYTHON=python3

install:
	${PYTHON} -m pip install .

test:
	${PYTHON} setup.py test

build:
	${PYTHON} setup.py build

publish:
	${PYTHON} setup.py publish
