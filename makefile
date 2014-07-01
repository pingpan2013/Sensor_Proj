
# makefile for cleaning all the .pyc files

clean:
	find . -name '*.pyc' -delete
	find . -name '*.*~' -delete
