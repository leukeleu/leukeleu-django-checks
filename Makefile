.PHONY: test devinstall unittests coveragetest coverage flaketest checkmanifest clean build check_tag release

test: flaketest coveragetest checkmanifest

devinstall:
	pip install --upgrade --upgrade-strategy eager -e .[test]

unittests:
	# Run unit tests with coverage
	coverage run ./runtests.py

coveragetest: unittests
	# Generate coverage report and require minimum coverage
	coverage report

coverage: unittests
	# Generate test coverage html report
	coverage html
	@echo "Coverage report is located at ./var/htmlcov/index.html"

flaketest:
	# Check syntax and style
	flake8

checkmanifest:
	# Check if all files are included in the sdist
	check-manifest

clean:
	# Remove build/dist dirs
	rm -rf build dist

build: test clean
	# Test, clean and build
	python setup.py build sdist bdist_wheel

check_tag:
	@echo "Did you bump the version number and tag a new version? [y/N] " && read ans && [ $${ans:-N} = y ]

release: check_tag build
	# Build and upload to PyPI
	twine upload dist/*
