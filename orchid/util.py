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

class Buffer:
	"""Text buffer supporting write function."""

	def __init__(self, text = ""):
		self.text = text

	def write(self, text):
		self.text = self.text + text

	def __str__(self):
		return self.text

def buffer(fun):
	"""Call function with a buffer to generate a text content and return
	the produced text."""
	buf = Buffer()
	fun(buf)
	return str(buf)
