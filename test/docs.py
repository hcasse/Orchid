#!/usr/bin/python3

"""Docs test."""

from urllib.parse import urlparse

import orchid as orc
from orchid import base
from orchid import group
from orchid import models
from orchid import listview

from orchid import doc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			doc.Pane([
				("doc1", "docs/doc1.html"),
				("doc2", "docs/doc2.html"),
				("doc3", "docs/doc3.html")
			]),
			app = app
		)

orc.Application("Docs Test", first=MyPage).run(debug=True)


