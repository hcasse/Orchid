#!/usr/bin/python3

"""Group align test."""

import orchid as orc

class MyPage(orc.Page):

	def __init__(self, app):
		orc.Page.__init__(
			self,
			orc.VGroup([

				orc.HGroup([
					orc.Label("HGroup"),
					orc.Button(label="ok"),
					orc.Label("align top"),
					orc.Button(label="ko"),
					orc.Label(orc.AssetImage("orchid.svg", width=32))
				], align=orc.Align.TOP),

				orc.HGroup([
					orc.Label("HGroup"),
					orc.Button(label="ok"),
					orc.Label("align bottom"),
					orc.Button(label="ko"),
					orc.Label(orc.AssetImage("orchid.svg", width=32))
				], align=orc.Align.BOTTOM),

				orc.HGroup([
					orc.Label("HGroup"),
					orc.Button(label="ok"),
					orc.Label("align center"),
					orc.Button(label="ko"),
					orc.Label(orc.AssetImage("orchid.svg", width=32))
				], align=orc.Align.CENTER),

				orc.HGroup([
					orc.Label("HGroup"),
					orc.Button(label="ok"),
					orc.Label("align justify"),
					orc.Button(label="ko"),
					orc.Label(orc.AssetImage("orchid.svg", width=32))
				], align=orc.Align.JUSTIFY),

				orc.HGroup([

					orc.VGroup([
						orc.Label("VGroup"),
						orc.Button(label="ok"),
						orc.Label("align left"),
						orc.Button(label="ko"),
						orc.Label(orc.AssetImage("orchid.svg", width=32))
					], align=orc.Align.LEFT),

					orc.VGroup([
						orc.Label("VGroup"),
						orc.Button(label="ok"),
						orc.Label("align right"),
						orc.Button(label="ko"),
						orc.Label(orc.AssetImage("orchid.svg", width=32))
					], align=orc.Align.RIGHT),

					orc.VGroup([
						orc.Label("VGroup"),
						orc.Button(label="ok"),
						orc.Label("align center"),
						orc.Button(label="ko"),
						orc.Label(orc.AssetImage("orchid.svg", width=32))
					], align=orc.Align.CENTER),

					orc.VGroup([
						orc.Label("VGroup"),
						orc.Button(label="ok"),
						orc.Label("align justify"),
						orc.Button(label="ko"),
						orc.Label(orc.AssetImage("orchid.svg", width=32))
					], align=orc.Align.JUSTIFY)
				])

			]),
			app = app
		)

orc.Application("Group Align Test", first=MyPage).run()

