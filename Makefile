PYTHON = python3
PACKAGE_NAME = ESXI-Control-System
VENV_DIR = .venv

SPHINX_BUILD = sphinx-build
HTML_DIR = docs/build/html
PDF_OUTPUT = docs/output.pdf


help:
	@echo "Available targets:"
	@echo "  setup - Set up the development environment"
	@echo "  activate - Activate the development environment"
	@echo "  install - Install the development environment dependencies"
	@echo "  test - Run unit tests"
	@echo "  create_docs - Generate project documentation as html"
	@echo "  build - Build the project and its dependencies into bin directory"
	@echo "  build_with_docker - Build the project inside a docker
	 container and export it to output directory to support cross platform"
	@echo "  clean - Remove temporary files"

setup:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_DIR)
	@echo "Virtual environment created."

activate:
	@echo "To activate the virtual environment, run:"
	. ./$(VENV_DIR)/bin/activate

install: setup 
	. ./$(VENV_DIR)/bin/activate && python3 -m pip install --upgrade pip
	. ./$(VENV_DIR)/bin/activate && pip install -r requirements.txt

test:
	@echo "Run the unit tests"
	. ./$(VENV_DIR)/bin/activate && python -m unittest discover -s tests
	sleep 2

create_docs:
	@echo "Add the following options: "
	@echo " > Separate source and build directories (y/n) [n]: n"
	@echo " > Project name: Calculator "
	@echo " > Author name(s): Elon Mask, Bill Gates "
	@echo " > Project release []: 0.0.1 "
	@echo " > Project language [en]: ar "
	sleep 5
	cd docs/; sphinx-quickstart
	
	sphinx-apidoc -o docs src/
	
	@echo "Edit the docs/conf.py file as follows: "
	@echo " - Add the following line at the begining of the file: "
	@echo "    import os, sys; sys.path.insert(0, os.path.abspath('../src'))"
	@echo " - Replace the line: extensions= [] with: "
	@echo "    extensions = ["sphinx.ext.todo", "sphinx.ext.viewcode", "sphinx.ext.autodoc"] "
	sleep 5

	nano docs/conf.py
	@echo "Edit the docs/index.py file if you have modules in your package as follows: "
	@echo " .. toctree:: "
	@echo " :maxdepth: 2 "
	@echo " :caption: Contents: "
	@echo " modules "
	sleep 5
	nano docs/index.rst
	cd docs/; make html

build: clean install 
	. ./$(VENV_DIR)/bin/activate && pyinstaller --onefile src/esxi_control_system.py --dist=bin
	mkdir bin/logs
	mkdir bin/conf
	cp conf/conf.json bin/conf/conf.json
	chmod +x bin/esxi_control_system
	rm -rf dist/ build/ esxi_control_system.spec

build_with_docker:
	docker build -t python_app_builder .
	docker run --rm -v "$(PWD)/output":/output python_app_builder
	mkdir output/logs
	mkdir output/conf
	cp conf/conf.json output/conf/conf.json

clean:
	rm -rf src/__pycache__ src/config_manager/__pycache__ src/remote_management/__pycache__ tests/__pycache__ bin/* logs/*