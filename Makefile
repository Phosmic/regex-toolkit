PYTHON=python3
APP_NAME=regex-toolkit

install:
	${PYTHON} -m pip install .

install-dev:
	${PYTHON} -m pip install -e .

test:
	@echo 'Running tests'
	${PYTHON} -m pytest tests
	@echo 'Done'

lint:
	@echo 'Linting code'
	${PYTHON} -m pylint src
	@echo 'Done'

format:
	@echo 'Formatting code'
	${PYTHON} -m isort src tests docs/render_readme.py
	${PYTHON} -m black src tests docs/render_readme.py
	@echo 'Done'

build:
	@echo 'Building package'
	${PYTHON} -m build
	@echo 'Done'

publish:
	@echo 'Building package'
	${PYTHON} -m build
	@echo 'Uploading package'
	${PYTHON} -m twine upload dist/${APP_NAME}-*.tar.gz dist/${APP_NAME}-*.whl
	@echo 'Done'

readme:
	@echo 'Generating README.md'
	${PYTHON} docs/render_readme.py
	@echo 'Done'
