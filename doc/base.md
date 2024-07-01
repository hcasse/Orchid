# Base Module

This module provides base classes for the rest of **Orchid** framework:

  * `Subject`, `Observer` implement *Subject-Observer* design pattern,
  * `Model` records resources used by each type of component,
  * `Component` represents any part of displayable and/or interactive part of the user interface,
  * `Page` includes resources and components used to show a user interface,
  * `Application` represents an application made of one or several pages.

Notice that these classes are just documented for features that relevant for the *User  Interface*. For internal work refer to [engine](engine.md).

## User Interface Work

The content of the UI is made of an HTML page that is send to the HTML browser. This content provides a display and a way to interact with components of the UI. Basically, events are captured in the browser and send back to the UI server. The receiver is a `Page` that, depending on the message, forwards it to the server-side component.

So when a page is generated, first the components are declared to the page that contains them by called `finalize`(page) method.This is used to declare the component to the page and to declare the used resources (called a component _Model_). Such a model is made of script code, script URLs to download, CSS content and CSS URL and may extend another model. The page ensures that these resources are downloaded once.

Then the generation phase starts. Basically a page is translated into an HTML page by calling the `gen`() function on page that is propagated to `gen`() function of components. This means that any component can generate an HTML element that may contain anything to manage itself. The parameter of these functions is called *out* and is basically an object supporting a function `write`(*text*) to write *text* to the resulting HTML.

After these generation phase, exchanges between the application and the HTTP client start (on behave of the client as it is enforced by HTTP protocol). From the client, these messages are used to trigger functions in the page or in the components (function `receive`(*message*, *handler*)). *message* is a dictionnary containing at least the key `id`, the identifier of the component it targets and a key `action` identifying the action the component has to undertake. Notice that other keys may also be passed.

To trigger such a message on the client side, **Orchid** provides a simple API based on function `ui_send`(*map*) with *map* corresponding to the *message* processed by `receive`() function. For example,
```html
<div onclick="send_ui(id:'3', action:'click')" .../> ... </div>
```
`send_ui` is typically called to react to a user trigger when an HTML event is activated.

On the Python side, the answer is usually a list of commands to update
the content of the HTML page:
  * adding/removing HTML elements, attributes and text,
  * adding/removing CSS attributes and classes,
  * add, change, remove its content,
  * invoking embedded Javascript functions.

This means that the HTML has an initial form at generation but its structure may evolve along and depending on the behaviour of the
components. In addition, as new components are added to displayed components, _model_ information of the added components may sent to the browser dynamically.

This exchange of messages, client-server requests and server-client answers, goes on until the *User Interface* stabilizes and restart on the next user interaction or if a timer function wake up on the client side.

In addition, components are alerted when they are displayed (function `on_show()`) or when they are hidden (function `on_hide()`).



## Models

An HTML page is made of several resources like:
  * CSS attributes,
  * Javascript functions.

A `Model` collect tese resources together and is attached to a component to provide them at generation time.

When a new component is designed, the model has to be passed to the `Component` base class. This information is then used by the HTML page generator to include are required resources.

In addition, as the `Component`sub-class have a hierarchic structure, the `Model` objects set up a parent link with the model of parent classes.

For example, the `group.HGroup` has for model `group.HGROUP_MODEL` and as `group.HGroup` from `group.Group`, `group.HGROUP_MODEL` has for parent `group.GROUP_MODEL`.

Therefore `Model`are usually singletons which value are provided at construction time. Below is an example of `group.HGROUP_MODEL`:

```python
HGROUP_MODEL = Model(
	parent = GROUP_MODEL,
	style = """
.hgroup-item {
}
.hgroup-expand {
	align-self: stretch;
}

.hgroup {
	display: flex;
	vertical-align: middle;
	flex-wrap: nowrap;
	column-gap: 4px;
	align-self: stretch;
	overflow: hidden;
}
"""
)
```

The configuration arguments supported by the constructor are:
  * `parent` -- parent model,
  * `style` -- CSS code to insert in HTML,
  * `script` -- Javascript code to in HTML,
  * `style_paths` -- paths to CSS file to insert in HTML,
  * `script_paths` -- paths to Javascript file to insert in HTML,


## Working with sessions

The application presented in [Quickstart](quickstart.md) works very well but is not adapted to work in a server context where several users may have their own session at the same time. In this case, one has to use a `Session` object. Each time a new client connects to the **Orchid** server a session and an index page is created.

The session is first used to manage the lifetime of the page that are used by the client. After some time without interaction from the client, the session pages are released.

For an application, it is a good starting point to manage the data associated with a particular client. This is why the session is created by the server by calling the function `new_session`(*manager*) in the `Application` class. This lets the application the opportunity to provide its own `Session` class extending the class `base.Session`.

Below is an example of an application providing a label and button. Each time the button is clicked, a counter is incremented and displayed on the page of the client performing the action.

```python
class MySession(Session):

	def __init__(self, app, man):
		Session.__init__(self, app, man)
		self.cnt = 0

	def get_index(self):
		self.label = Label("0")
		return Page(
			VGroup([
				Label("Session %d" % self.get_number()),
				self.label,
				Button("Increment", on_click=self.on_click)
			]),
			app = self.app
		)

	def on_click(self):
		self.cnt += 1
		self.label.set_text(str(self.cnt))


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "session-test")

	def new_session(self, man):
		return MySession(self, man)
```


## Component

A component represents a part of the display and may be interactive. It generates its content, as an HTML content, with the function: `gen`(*self*, *out*).

The generated HTML code of a component can be customied with functions like:
  * `set_style`(*attr*, *value*) -- to set a CSS attribute,
  * `add_class`(*class*) -- to add a CSS class,
  * `remove_class`(*class*) -- to remove a CSS class.
  * `set_attr`(*attr*, *value*) -- to set an HTML attribute,
  * `remove_attr`(*attr*) -- to remove an HTML attribute,
  * `append_content`(*content*) -- append content to the component element,
  * `insert_content`(*content*, *position*) -- insert at the *position*,
  * `remove_content`(*position*) -- remove content at position,
  * `clear_content`() -- clear the content of the element.
  * `call`(*function*, *arguments*) -- call the Javascript *function* in the target HTML page with the given arguments. Notice that the called function takes only one argument: the dictionary passed as *arguments*.

Notice that all these function takes an optional argument that allows to select the identifier of a sub-element of the component element.

**Example:** call
In the component,

	def on_event(self):
		self.call("my_function", {"msg": "hello", "times": 4})

In the page,

```python
	function my_function(args) {
		for(var i = 0; i < args.times; i++)
			console.log(args.msg);
	}
```

Notice that these functions can be called off-line and will be passed automatically to the HTTP client once the page has been generated. If class, style and attribute setting can also be passed off-line but will be inserted in the generated HTML page with `gen_attrs`(*out*), typically after the element tag:

```python
def gen(self, out):
	out.write("<div ");
	self.gen_attrs();
	out.write(">")
	...
	out.write("</div>")
```

As presented before, messages from the HTTP client are handled with the function:

	`receive`(*self*, *msg*, *handler*)

Where *msg* is a dictionary containing at least the `action` field which value is dependent on the application. The *handler* is an HTTPHandler as provided by the standard Python library and may be used, for example, for logging.

Components provides also functions to manage the geometry of the component (that may be override by sub-classes):
  * `expands_horizontal`() -- if the component can horizontally,
  * `expands_vertical`() -- if the component can vertical,
  * `get_weight`() -- weight describing the place taken the component.

Instead of overloading `get_weight`(), one can also juste set the `weight` attribute.

State of the component can be changed with function:
  * `enable()`,
  * `disable()`,
  * `set_enabled`(*enabled*),
  * `show()`,
  * `hide()`.

Components provide also global information:
  * `get_id`(),
  * `get_page`(),
  * `online`() -- returns true if the page is online.


## Javascript

Communication with server-side application is performed using standard HTTP requests. The answers are centered in a specific function that implements several commands that may be used by Python components to update the state of the displayed HTML page.

On the client-side, the following Javascript functions are available:
	* `ui_close`() -- close the current page,
	* `ui_complete`() -- send the posted message to the server,
	* `ui_open`(*URL*) -- replace the current page by the given URL,
	* `ui_post`(*message*) -- add a message to the list of messages to send to the server,
	* `ui_send`(*message*) -- `ui_post` then `ui_complete`.

The send message is a Javascript map containing at least the field `id` with the identifier of the target component.



