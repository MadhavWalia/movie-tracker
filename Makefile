test:
	pytest . -v

fmt:
	black .
	isort -rc .
	autoflake .