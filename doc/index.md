# Orchid Manual

**Orchid** is a Python environment to develop HTML-based user interfaces.


## Hellow World!

```python
import orchid
from orchid import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				Label("Hello, World!"),
				Button("Quit", on_click=self.close)
			]),
			app = app
		)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "MyApp",
			version="1.0",
			authors=["M. Self <self@here.org>"],
			license="GPL 2.1",
			copyright="Copyright (c) 2021 M. Self <self@here.org",
			description="This is my application.")

	def first(self):
		return MyPage(self)

orchid.run(MyApp())
```

This small program will open a browser that displays a single label
"Hello, World!" and a single button to close the window.

The class ``MyPage`` defines the lookup and the components of the displayed
page: it is a vertical stack made of a label and of a button. In turn,
the button, when clicked, invokeds the ``close`` function of the page.

All is embedded in in an application, ``MyApp` which attributes are
defined in the constructor. The important function here is ``first``
that returns the first page of the application.

Finally, the last line runs the **Orchid** server on the application.


## Getting autodoc

```
	$ pydoc3.8 -b orchid
```
