PYTHON=python3

install:
	${PYTHON} -m pip install .

install-dev:
	${PYTHON} -m pip install -e .

test:
	${PYTHON} -m pytest tests

lint:
	${PYTHON} -m pylint src

format:
	${PYTHON} -m isort src tests docs/render_readme.py
	${PYTHON} -m black src tests docs/render_readme.py

build:
	@echo 'Building package'
	${PYTHON} -m build
	@echo 'Done'

publish:
	@echo 'Building package'
	${PYTHON} -m build
	@echo 'Uploading package'
	${PYTHON} -m twine upload dist/yogger-*.tar.gz dist/yogger-*.whl
	@echo 'Done'

readme:
	@echo 'Generating README.md'
	@cd docs && ${PYTHON} render_readme.py
	@echo 'Copying README.md'
	@cp ./docs/README.md ./README.md
	@echo 'Done'
