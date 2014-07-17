all:
	python -c "import inspect; import antenna; print inspect.getdoc(antenna)" > README.md
	pandoc -o README.rst README.md