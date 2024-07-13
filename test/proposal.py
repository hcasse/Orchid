#!/usr/bin/python3

"""Proposal field test."""

import orchid as orc

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

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([
				orc.ProposalField(label="Proposal", propose=self.propose),
				orc.EmailField(label="Email", place_holder="Email"),
				orc.Editor(init="my editor!")
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


orc.Application("Proposal Field Test", first=MyPage).run()

