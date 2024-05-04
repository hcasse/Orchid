#!/usr/bin/python3

from orchid import *

class MyPage(Page):

	def __init__(self, app):
		Page.__init__(
			self,
			VGroup([

				HGroup([
					Label("HGroup"),
					Button(label="ok"),
					Label("align top"),
					Button(label="ko"),
					Label(AssetImage("orchid.svg", width=32))
				], align=ALIGN_TOP),

				HGroup([
					Label("HGroup"),
					Button(label="ok"),
					Label("align bottom"),
					Button(label="ko"),
					Label(AssetImage("orchid.svg", width=32))
				], align=ALIGN_BOTTOM),

				HGroup([
					Label("HGroup"),
					Button(label="ok"),
					Label("align center"),
					Button(label="ko"),
					Label(AssetImage("orchid.svg", width=32))
				], align=ALIGN_CENTER),

				HGroup([
					Label("HGroup"),
					Button(label="ok"),
					Label("align justify"),
					Button(label="ko"),
					Label(AssetImage("orchid.svg", width=32))
				], align=ALIGN_JUSTIFY),

				HGroup([

					VGroup([
						Label("VGroup"),
						Button(label="ok"),
						Label("align left"),
						Button(label="ko"),
						Label(AssetImage("orchid.svg", width=32))
					], align=ALIGN_LEFT),

					VGroup([
						Label("VGroup"),
						Button(label="ok"),
						Label("align right"),
						Button(label="ko"),
						Label(AssetImage("orchid.svg", width=32))
					], align=ALIGN_RIGHT),

					VGroup([
						Label("VGroup"),
						Button(label="ok"),
						Label("align center"),
						Button(label="ko"),
						Label(AssetImage("orchid.svg", width=32))
					], align=ALIGN_CENTER),

					VGroup([
						Label("VGroup"),
						Button(label="ok"),
						Label("align justify"),
						Button(label="ko"),
						Label(AssetImage("orchid.svg", width=32))
					], align=ALIGN_JUSTIFY)
				])

			]),
			app = app
		)

class MyApp(Application):

	def __init__(self):
		Application.__init__(self, "Group Align Test")
		self.fst = MyPage(self)

	def first(self):
		return self.fst

run(MyApp(), debug=True)

