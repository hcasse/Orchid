PYLINT=pylint

export PYTHONPATH=$(PWD)

all:

check:
	$(PYLINT) orchid | less

autodoc:
	gnome-terminal -- pydoc3 -b
