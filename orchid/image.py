"""Management of images."""

from orchid.base import Model, CONTEXT_HEADERBAR, CONTEXT_NONE

class Image:
	"""Base class to represent an image (according different sources:
	file to download, standard icon, etc)."""

	def __init__(self, model):
		self.model = model

	def get_model(self):
		return self.model

	def gen(self, out, type = CONTEXT_NONE):
		"""Generate the code for the image."""
		pass


class IconModel(Model):

	def get_style_paths(self):
		return ["bootstrap-icons/bootstrap-icons.css"]
		

ICON_MODEL = IconModel()

BOOTSTRAP_ICONS = {

	# actions
	"add": "plug-lg",
	"align-left": "text-left",
	"align-right": "text-right",
	"center": "text-center",
	"chat": "chat-dots",
	"check": "check",
	"check-all": "check-all",
	"configure": "wrench-adjustable",
	"cut": "scissors",
	"debug": "bug-fill",
	"download": "cloud-download",
	"eject": "eject-fill",
	"enter": "box-arrow-in-right",
	"erase": "eraser-fill",
	"fast-forward": "fast-forward-fill",
	"go-back": "back",
	"go-forward": "forward-fill",
	"go-front": "front",
	"go-home": "house-fill",
	"indent": "text-indentleft",
	"justify": "justify",
	"leave": "box-arrow-right",
	"paint": "brush-fill",
	"pause": "pause-fill",
	"pick": "eyedropper",
	"pin": "pin-angle-fill",
	"play": "play-fill",
	"print": "printer-fill",
	"process": "gear",
	"protect": "shield-fill-check",
	"quit": "power",
	"record": "record-fill",
	"remove": "x-lg",
	"repeat": "repeat",
	"reply": "reply-fill",
	"rewind": "rewind-fill",
	"search": "search",
	"send": "send",
	"show": "eye",
	"shuffle": "shuffle",
	"skip-backward": "skip-backward-fill",
	"skip-end": "skip-end-fill",
	"skip-forward": "skip-forward-fill",
	"skip-start": "skip-start-fill",
	"sort-alpha-down": "sort-alpha-down",
	"sort-alpha-up": "sort-alpha-up",
	"stop": "stop-fill",
	"unindent": "text-indent-right",
	"uplodad": "cloud-upload",
	"work": "hammer",
	"zoom-in": "zoom-in",
	"zoom-out": "zoom-out",

	# decorators
	"add-docrator": "plus-circle-fill",
	"remove-docrator": "x-circle-fill",

	# symbols
	"angry": "emoji-angry",
	"happy": "emoji-smile",
	"help": "life-preserver",
	"info": "info-circle-fill",
	"neutral": "emoji-neutral",
	"question": "question-circle-fill",
	"quote": "quote",
	"warning": "exclamation-triangle-fill",

	# keys
	"arrow-down": "caret-down-fill",
	"arrow-left": "caret-left-fill",
	"arrow-right": "caret-right-fill",
	"arrow-up": "caret-up-fill",
	"backspace": "backspace-fill",
	"braces": "braces",
	"shift": "shift-fill",

	# objects
	"alarm": "bell-fill",
	"bookmark": "bookmark-fill",
	"bookmarks": "bookmarks-fill",
	"box": "box2-fill",
	"calendar": "calendar",
	"camera": "camera-reels-fill",
	"clock": "clock",
	"doc": "book-fill",
	"drop": "droplet-fill",
	"event": "calendar-event",
	"flag": "flag-fill",
	"fullscreen": "fullscreen",
	"graph": "diagram-3-fill",
	"idea": "lighbulb",
	"image": "image",
	"key": "key",
	"lock": "lock-fill",
	"map": "map",
	"message": "envelope",
	"money": "cash-coin",
	"music": "music-note-beamed",
	"people": "people-fill",
	"person": "person-fill",
	"piece": "puzzle",
	"point": "geo-alt-fill",
	"star-empty": "star",
	"star-full": "star-fill",
	"stats": "bar_char_line-fill",
	"stopwatch": "stopwatch",
	"tag": "tag",
	"thrashcan": "thrash",
	"todo": "clipboard-check",
	"wall": "bricks",

	# technology
	"database": "database",
	"ethernet": "ethernet",
	"file": "file-earmark",
	"folder": "folder",
	"harddisk": "device-hdd",
	"headphones": "headphones",
	"keyboard": "keyboard",
	"micro": "mic",
	"mouse": "mouse-fill",
	"printer": "printer-fill",
	"screen": "display",
	"terminal": "terminal",
	"usbkey": "device-ssd",
	"wifi": "wifi",
	"window": "window"
}

ICONS = BOOTSTRAP_ICONS

class Icon(Image):
	"""An image using standard icons as defined in the documentation.
	If the icon name starts with "!", the named is looked in the
	current icon collection (https://icons.getbootstrap.com/)."""

	def __init__(self, name):
		Image.__init__(self, ICON_MODEL)
		self.name = name

	def gen(self, out, context):
		if self.name.startswith("!"):
			icon = self.name[1:]
		else:
			icon = ICONS[self.name]
		out.write('<i class="bi bi-%s' % icon)
		if context == CONTEXT_HEADERBAR:
			out.write(' headerbar-icon')
		out.write('"></i>')
