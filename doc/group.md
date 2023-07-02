# Groups

The components described here are contained in module `orchid.group`.

Groups allows to arrange other components horizontally -- `HGroup` or vertically -- `VGroup`. According to their direction, they work in the same way.

Their constructor takes a list of components they will display in this order:

	group = HGroup([
		Button(label="Button 1"),
		Button(label="Button 2"),
		Button(label="Button 3")
	])


Basically the components, depending on their weight, occupies the whole space devoted to the group. Basically, their place is determined by their weight (obtained by the function `get_weight`() that returns a pair ( *horizontal weight*, *vertical weight* ). Only the item corresponding to the direction of the group is used, thereafter simply called *weight*.

If no weight is defined for a component, they calculated from functions `expands_horizontal`() or `expands_vertical`() depending on the group direction. Another way to assign a *weight* to a component is to assign the `weight` attribute of the component.

The *weights* are used as CSS `flex-grow` parameter (https://www.w3schools.com/cssref/css3_pr_flex-grow.php) that, to be short, assigns a minimal place to each component and share the remaining according to the weights.

Inserting blanks in the group, for example to implement left/right/center alignment or other, can be achieved using `Spring` objects. They represents invisible objects that allocates place according to their constructor parameters:
  * `hexpand` -- if True, expands horizontally
  * `vexpand` -- if True, expands vertically
  * `weight` -- weight of the spring in both direction depending on `hexpand` and `vexpand`.

So, for example, to have some buttons to the left and other buttons aligned right, you can write:


	HGroup([
		Button(label="File"),
		Button(label="Edit"),
		Button(label="View"),
		Spring(hexpand = True, weight=1),
		Button(label="Help"),
		Button(label="About")
	])


