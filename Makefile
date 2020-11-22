check:
	pycodestyle .
	flake8 .

test:
	pytest -v --cov --doctest-modules

cov: test
	codecov

format:
	yapf --recursive -i py_hcl tests examples

clean:
	rm -rf .eggs dist py_hcl.egg-info .coverage .pytest_cache */__pycache__

upload: test
	python setup.py sdist && twine upload dist/*