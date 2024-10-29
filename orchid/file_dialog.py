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

"""Module providing a file dialog for the host file system. A file dialog allows
to select 1/n file/directory. The displayed files can be filtered using patterns
from file system sources. These sources can filtered view of the real file system
like sandbox directories."""

from orchid.base import Model
from orchid.dialog import Base

class Source:
	"""Source provides a file system."""
	pass

class Dialog(Base):
	"""Display a file dialog. It is defined by:
	* title - title of the dialog,
	* text - explanation for the dialog,
	* existing - if True, the file/directory must exist,
	* file - if true, this must be file (a directory else),
	* multiple - multiple selection is supported,
	* patterns - patterns to filter the file,
	* sources - file system sources.
	"""

	MODEL = Model("file-dialog")

	def __init__(self,
		title="",
		text="",
		file=True,
		existing=False,
		multiple=False,
		patterns=None,
		sources=None
	):
		pass
