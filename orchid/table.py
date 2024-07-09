"""Orchid module in charge of table display."""

from orchid.base import Component, Model
from orchid.models import TableModel, ListTableModel, TableObserver
from orchid.util import Buffer

ACTION_TR	= 0		# TR number
ACTION_TD	= 1		# TD number
ACTION_SET	= 2		# set count
ACTION_REMOVE = 3	# no value
ACTION_APPEND = 4	# TD count
ACTION_INSERT = 5	# TD count


class TableView(Component, TableObserver):
	"""Represents a table made of rows and columns."""

	MODEL = Model(
		script_paths = [ "table.js" ],
		style="""
#table-edit {
	border: none;
	padding: 0;
	margin: 0;
	box-sizing: bodrer-box;
	width: 0;
	min-width: 100%;
}

.table-error {
	background-color: peachpuff;
}
"""
)

	def __init__(self,
		table,
		no_header = False,
		model = None,
		format = lambda row, col, val: str(val),
		parse = lambda row, col, val: val,
		headers = None
	):
		"""Initialize a table. The passed argument may a 2-dimension
		Python list or an instance of table.Model.

		Format and parse arguments are functions, respectively to format
		and parse table values as performed by format_cell() and parse_cell().
		Parse has to return None if the value cannot be parsed."""
		if model is None:
			model = self.MODEL
		Component.__init__(self, model)
		self.no_header = no_header
		if isinstance(table, TableModel):
			self.table = table
		else:
			self.table = ListTableModel(table)
		self.add_class("table")
		self.set_style("align-self", "start")
		self.add_class("text-back")
		self.last_row = None
		self.last_col = None
		self.last_value = None
		self.shown = False
		self.format = format
		self.parse = parse
		self.headers = headers
		if self.headers is None:
			self.no_header = True

	def on_show(self):
		self.table.add_observer(self)
		self.shown = True

	def on_hide(self):
		self.table.remove_observer(self)
		self.shown = False

	def get_table_model(self):
		"""Get the table model."""
		return self.table

	def set_table_model(self, model):
		"""Change the model of the table."""

		# setup the data structure
		if self.online() and self.is_shown():
			self.table.remove_observer(self)
		if isinstance(model, TableModel):
			self.table = model
		else:
			self.table = ListTableModel(model)
		if self.online() and self.shown:
			self.table.add_observer(self)

		# if required, generate its content
		self.on_table_set(self.table)

	def gen_content(self, out):
		"""Generate the content of the table."""
		coln = self.table.get_column_count()

		# if any, generate header
		if not self.no_header:
			out.write('<tr class="table-header">')
			for col in range(0, coln):
				out.write(f"<th>{self.headers[col]}</th>")
			out.write("</tr>")

		# generate the content
		for row in range(0, self.table.get_row_count()):
			out.write("<tr>")
			for col in range(0, coln):
				val = self.table.get_cell(row, col)
				out.write(f"<td>{self.format(row, col, val)}</td>")
			out.write("</tr>")

	def on_table_set(self, table):
		if self.online():
			buf = Buffer()
			self.gen_content(buf)
			self.set_content(str(buf))

	def gen(self, out):
		out.write(f'<table onclick="table_on_click(\'{self.get_id()}\', event);"')
		self.gen_attrs(out)
		out.write(">")
		self.gen_content(out)
		out.write("</table>")

	def on_cell_set(self, table, row, col, val):
		"""Called by the model to update a cell value."""
		if self.online():
			act_row = row if self.no_header else row+1
			val = self.table.get_cell(row, col)
			self.call("table_change", {
				"id": self.get_id(),
				"actions": [ ACTION_TR, act_row, ACTION_TD, col, ACTION_SET, 1 ],
				"values" : [ self.format(row, col, val) ]
			})

	def on_row_append(self, table, vals):
		"""Called by the model to append a new row."""
		cnt = len(vals)
		row = self.table.get_row_count()-1
		self.call("table_change", {
			"id": self.get_id(),
			"actions": [
				ACTION_APPEND, cnt,
				ACTION_SET, cnt
			],
			"values": [self.format(row, col, x) for (col, x) in enumerate(vals)]
		})

	def on_row_insert(self, table, row, vals):
		"""Called by the model to insert a new row."""
		cnt = len(vals)
		act_row = row if self.no_header else row+1
		self.call("table_change", {
			"id": self.get_id(),
			"actions": [
				ACTION_TR, act_row,
				ACTION_INSERT, cnt,
				ACTION_SET, cnt
			],
			"values": [self.format(row, col, x) for (col, x) in enumerate(vals)]
		})

	def on_row_remove(self, table, row):
		"""Called by the model to remove a row."""
		act_row = row if self.no_header else row+1
		self.call("table_change", {
			"id": self.get_id(),
			"actions": [
				ACTION_TR, act_row,
				ACTION_REMOVE
			],
			"values": []
		})

	def check_edit(self, val):
		if self.last_row is not None:
			val = self.parse(self.last_row, self.last_col, val)
			if val is not None:
				self.table.set(self.last_row, self.last_col, val)
			else:
				val = self.table.get_cell(self.last_row, self.last_col)
				self.on_cell_set(self.table, self.last_row, self.last_col, val)
		self.last_row = None
		self.last_col = None
		self.last_value = None

	def receive(self, msg, handler):
		action = msg["action"]

		# click: start editing
		if action == "is_editable":
			if self.last_value is not None:
				self.check_edit(self.last_value)
			row, col = msg["row"], msg["col"]
			if not self.no_header:
				row -= 1
			if self.table.is_editable(row, col):
				self.last_row = row
				self.last_col = col
				self.call("table_do_edit", {})

		# check and validation
		elif action == "check":
			self.check_edit(msg["value"])

		# test if current value is ok
		elif action == "test":
			self.last_value = msg["value"]
			value = self.parse(self.last_row, self.last_col, self.last_value)
			if value is not None:
				self.call("table_set_ok", {})
			else:
				self.call("table_set_error", {})

		# default behaviour
		else:
			Component.receive(self, msg, handler)
