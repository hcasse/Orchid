"""Implements a tabbed pane.

All children are stacked and only is visible at time.
A children may become visible by calling set_tab() function or
according to the user that can click on the corresponding tab header.
The tab header label are obtained from an attribute "tab_title"
defined in the child.
"""

# https://www.w3schools.com/howto/howto_js_tabs.asp

from orchid.base import *
from orchid.group import *

TAB_PANE_MODEL = Model(
	style="""
.tabpane {
	overflow: hidden;
	border: 1px solid #ccc;
	background-color: #f1f1f1;
}

.tabpane .head button {
	background-color: inherit;
	float: left;
	border: none;
	outline: none;
	cursor: pointer;
	padding: 14px 16px;
	transition: 0.3s;
}

.tabpane .head button:hover {
	background-color: #ddd;
}

.tabpane .head button.active {
	background-color: #ccc;
}

.tabpane .content {
	display: none;
	padding: 6px 12px;
	border: 1px solid #ccc;
	border-top: none;
}
""",
	script="""
function tabpane_select(id, num) {
	var content = document.getElementsByClassName("${id}-content");
	for(i = 0; i < content.length; i++)
		content[i].style.display = "none";
	var links = document.getElementsByClassName("${id}-links");
	for(i = 0; i < links.length; i++)
		links[i].className = links[i].className.replace(" active", "");
	content[num].style.display = "block";
	links[num].className += " active";
}
"""
)

class TabPane(Group):

	def __init__(self, model, comps):
		Group.__init__(self, model, comps)
		self.add_class("tabpane")
		num = 0
		for comp in comps:
			if not hasattr(comp, "tab_title"):
				comp.tab_title = "tab %d" % num
				num = num + 1

	def gen(self, out):
		out.write('<div ')
		self.gen_attrs(out)
		out.write('>\n')
		id = self.get_id()
		
		# generate header
		out.write("<div class='head' id='%s-links'>\n" % id)
		num = 0
		for child in self.children:
			out.write('<button onclick="tabpane_select(%s, %d)">%s</button>\n' % (id, num, child.tab_title))
			num = num + 1
		out.write("</div>\n")

		# generate content
		out.write("<div class='content' id='%s-content'>\n" % id)
		for c in self.children:
			c.gen(out)
		out.write("</div>\n")

		out.write("</div>\n")
