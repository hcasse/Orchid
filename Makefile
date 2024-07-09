PYLINT=pylint

export PYTHONPATH=$(PWD)

all:

check:
	$(PYLINT) orchid | less
