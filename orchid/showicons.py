#
#	This file is part of Orchid.
#
#    Orchid is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Lesser General Public License as
#	published by the Free Software Foundation, either version 3 of the
#	License, or (at your option) any later version.
#
#	Orchid is distributed in the hope that it will be useful, but
#	WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#	GNU Lesser General Public License for more details.
#
#	You should have received a copy of the GNU Lesser General Public
#	License along with Orchid. If not, see <https://www.gnu.org/licenses/>.
#

"""Open a window showing icons."""

from orchid import Page, Application, VGroup, Button, Icon, IconType, HGroup

class MyPage(Page):

	def __init__(self, app: Application):

		groups = [ ]
		buts = [ ]
		for type in IconType:
			if len(buts) == 8:
				groups.append(HGroup(buts))
				buts = []
			buts.append(Button(f"IconType.{type.name}", image=Icon(type)))

		Page.__init__(
			self,
			VGroup(groups),
			app = app
		)

Application("Show Icons", first=MyPage).run(standalone = True)


