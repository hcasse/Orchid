# Quickstart

**Orchid** is a Python environment to develop HTML-based user interfaces.


## Hellow World!

```python
import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.Label("Hello, World!"),
				orc.Button("Quit", on_click=self.close)
			]),
			app = app
		)

orc.Application(
	"MyApp",
	version="1.0",
	authors=["M. Self <self@here.org>"],
	license="GPL 2.1",
	copyright="Copyright (c) 2021 M. Self <self@here.org",
	description="This is my application.",
	first=MyPage).run()
```

This small program will open a browser that displays a single label "Hello, World!" and a single button to close the window.

The class `MyPage` defines the lookup and the components of the displayed page: it is a vertical stack made of a label and of a button. In turn, the button, when clicked, invokes the `close` function of the page.

All is embedded in in an application which attributes are defined in the constructor. The important parameter here is `first` that provides the constructor of first page of the application.

Finally, after constructing the application, the **Orchid** server server is started and the page will be displayed in your preferred server.


## Getting autodoc

```
	$ pydoc3 -b
```


## Customizing the display

All components comes with their own HTML class. Defining a new lookup consists in replacing `basic.css` with a new file where the component classes are changed.



