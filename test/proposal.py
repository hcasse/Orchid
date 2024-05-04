#!/usr/bin/python3

from orchid import *
from orchid.field import ProposalField

TEXTS = [
	"this",
	"is",
	"just",
	"a",
	"test",
	"of",
	"proposal",
	"isn't",
	"it"
]

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([
				ProposalField(label="Proposal", propose=self.propose),
				EmailField(label="Email", place_holder="Email"),
				Editor(init="my editor!")
			]),
			app = app
		)

	def propose(self, value):
		res = []
		for text in TEXTS:
			if value in text:
				res.append(text)
				if len(res) >= 4:
					break
		return res


class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "MyApp")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

