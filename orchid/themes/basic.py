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

"""Definition of basic theme."""

from orchid.base import Model, Context, Theme
from orchid.image import AssetImage, Image, IconType

MESSAGES = {
	"warning": "basic/warning.svg",
	"error": "basic/error.svg",
	"info": "basic/info.svg"
}

BOOTSTRAP_ICONS = {

	# actions
	IconType.ABOUT: "info-lg", #!
	IconType.ADD: "plus-lg",
	IconType.ALIGN_LEFT: "text-left",
	IconType.ALIGN_RIGHT: "text-right",
	IconType.CENTER: "text-center",
	IconType.CHAT: "chat-dots",
	IconType.CHECK: "check",
	IconType.CHECK_ALL: "check-all",
	IconType.CONFIGURE: "tools",
	IconType.CONTEXT_MENU: "three-dots-vertical",
	IconType.CUT: "scissors",
	IconType.DEBUG: "bug-fill",
	IconType.DOWNLOAD: "cloud-download",
	IconType.EJECT: "eject-fill",
	IconType.ENTER: "box-arrow-in-right",
	IconType.ERASE: "eraser-fill",
	IconType.FAST_FORWARD: "fast-forward-fill",
	IconType.GO_BACK: "back",
	IconType.GO_FORWARD: "forward-fill",
	IconType.GO_FRONT: "front",
	IconType.GO_HOME: "house-fill",
	IconType.INDENT: "text-indentleft",
	IconType.JUSTIFY: "justify",
	IconType.LEAVE: "box-arrow-right",
	IconType.MENU: "list",
	IconType.PAINT: "brush-fill",
	IconType.PAUSE: "pause-fill",
	IconType.PICK: "eyedropper",
	IconType.PIN: "pin-angle-fill",
	IconType.PLAY: "play-fill",
	IconType.PRINT: "printer-fill",
	IconType.PROCESS: "gear",
	IconType.PROTECT: "shield-fill-check",
	IconType.QUIT: "power",
	IconType.RECORD: "record-fill",
	IconType.REMOVE: "x-lg",
	IconType.REPEAT: "repeat",
	IconType.REPLY: "reply-fill",
	IconType.RESET: "bootstrap-reboot",	#!
	IconType.REWIND: "rewind-fill",
	IconType.SEARCH: "search",
	IconType.SEND: "send",
	IconType.SHOW: "eye",
	IconType.SHUFFLE: "shuffle",
	IconType.SKIP_BACKWARD: "skip-backward-fill",
	IconType.SKIP_END: "skip-end-fill",
	IconType.SKIP_FORWARD: "skip-forward-fill",
	IconType.SKIP_START: "skip-start-fill",
	IconType.SORT_DOWN: "sort-alpha-down",
	IconType.SORT_UP: "sort-alpha-up",
	IconType.STOP: "stop-fill",
	IconType.UNINDENT: "text-indent-right",
	IconType.UPLOAD: "cloud-upload",
	IconType.WORK: "hammer",
	IconType.ZOOM_IN: "zoom-in",
	IconType.ZOOM_OUT: "zoom-out",

	# decorators
	IconType.ADD_DECO: "plus-circle-fill",
	IconType.REMOVE_DECO: "x-circle-fill",

	# symbols
	IconType.ANGRY: "emoji-angry",
	IconType.FEMALE: "geneder-female",	#!
	IconType.HAPPY: "emoji-smile",
	IconType.HELP: "life-preserver",
	IconType.INFO: "info-circle-fill",
	IconType.LAYERS: "layers",		# !
	IconType.MALE: "gender-male",		# !
	IconType.NEUTRAL: "emoji-neutral",
	IconType.QUESTION: "question-circle-fill",
	IconType.QUOTE: "quote",
	IconType.WARNING: "exclamation-triangle-fill",

	# keys
	IconType.ARROW_DOWN: "caret-down-fill",
	IconType.ARROW_LEFT: "caret-left-fill",
	IconType.ARROW_RIGHT: "caret-right-fill",
	IconType.ARROW_UP: "caret-up-fill",
	IconType.BACKSPACE: "backspace-fill",
	IconType.BRACES: "braces",
	IconType.SHIFT: "shift-fill",

	# objects
	IconType.ALARM: "bell-fill",
	IconType.BOOKMARK: "bookmark-fill",
	IconType.BOOKMARKS: "bookmarks-fill",
	IconType.BOX: "box2-fill",
	IconType.CALENDAR: "calendar",
	IconType.CAMERA: "camera-reels-fill",
	IconType.CLOCK: "clock",
	IconType.DOC: "book-fill",
	IconType.DROP: "droplet-fill",
	IconType.EVENT: "calendar-event",
	IconType.FIRE: "fire",				# !
	IconType.FLAG: "flag-fill",
	IconType.FLOWER: "flower1",		# !
	IconType.FULLSCREEN: "fullscreen",
	IconType.GRAPH: "diagram-3-fill",
	IconType.HOURGLASS: "hourglass-split",	# !
	IconType.IDEA: "lighbulb",
	IconType.IMAGE: "image",
	IconType.KEY: "key",
	IconType.LOCK: "lock-fill",
	IconType.MAGIC: "magic",	#!
	IconType.MAP: "map",
	IconType.MESSAGE: "envelope",
	IconType.MONEY: "cash-coin",
	IconType.MUSIC: "music-note-beamed",
	IconType.PEOPLE: "people-fill",
	IconType.PALETTE: "palette",	 	#!
	IconType.PAPERCLIP: "paperclip",	#!
	IconType.PENCIL: "pencil", #!
	IconType.PERSON: "person-fill",
	IconType.PIECE: "puzzle",
	IconType.PROJECT: "box2-fill",
	IconType.PLUG: "plug",		#!
	IconType.POINT: "geo-alt-fill",
	IconType.STACK: "stack",	#!
	IconType.STAR_EMPTY: "star",
	IconType.STAR_FULL: "star-fill",
	IconType.STATS: "bar_char_line-fill",
	IconType.STOPWATCH: "stopwatch",
	IconType.TAG: "tag",
	IconType.TARGET: "bullseye",	#++
	IconType.TRASHCAN: "thrash",
	IconType.TODO: "clipboard-check",
	IconType.WALL: "bricks",
	IconType.VIRUS: "virus",	#!

	# technology
	IconType.CODE: "code",		#!
	IconType.CPU: "cpu",		#!
	IconType.DATABASE: "database",
	IconType.DESKTOP: "pc-display",	#!
	IconType.ETHERNET: "ethernet",
	IconType.FILE: "file-earmark",
	IconType.FOLDER: "folder",
	IconType.HARDDISK: "device-hdd",
	IconType.HEADPHONES: "headphones",
	IconType.KEYBOARD: "keyboard",
	IconType.LAPTOP: "laptop",	#!
	IconType.LINK: "link", #!
	IconType.MICRO: "mic",
	IconType.MOUSE: "mouse-fill",
	IconType.PRINTER: "printer-fill",
	IconType.SCREEN: "display",
	IconType.TERMINAL: "terminal",
	IconType.USBKEY: "device-ssd",
	IconType.WIFI: "wifi",
	IconType.WINDOW: "window"
}

ICONS = BOOTSTRAP_ICONS

ICON_MODEL = Model("basic.icon-model")

class Icon(Image):
	"""An image using standard icons as defined in the documentation.
	If the icon name starts with "!", the named is looked in the
	current icon collection (https://icons.getbootstrap.com/)."""

	CONTEXT = {
		Context.HEADERBAR: " headerbar-icon",
		Context.TOOLBAR: " toolbar-icon",
		Context.STATUSBAR: " statusbar-icon"
	}

	def __init__(self, type, color = None):
		Image.__init__(self, ICON_MODEL)
		self.type = type
		self.color = color

	def gen(self, out):
		self.gen_in_context(out, Context.NONE)

	def gen_in_context(self, out, context):
		if isinstance(self.type, str) and self.type.startswith('!'):
			icon = self.type[1:]
		else:
			try:
				icon = ICONS[self.type]
			except KeyError:
				icon = ICONS[IconType.IMAGE]
		out.write(f'<i class="bi bi-{icon}')
		try:
			out.write(Icon.CONTEXT[context])
		except KeyError:
			out.write(" default-icon")
		out.write('"')
		if self.color is not None:
			out.write(f' style="color: {self.color}"')
		out.write('"></i>')


class BasicTheme(Theme):

	def __init__(self):
		Theme.__init__(self, "basic", style_paths=[
			"basic.css",
			"bootstrap-icons/bootstrap-icons.css"
		])

	def get_icon(self, type, color=None):
		return Icon(type, color)

	def get_dialog_icon(self, type, size=32):
		if type in MESSAGES:
			return AssetImage(MESSAGES[type], width=size)
		else:
			return None


def get():
	"""Get an instance of this theme."""
	return BasicTheme()
