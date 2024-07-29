"""Orchid module in charge of table display."""

from orchid.base import Component, Model
from orchid.models import TableModel, ListTableModel, TableObserver
from orchid.util import Buffer, Context

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

div.table {
	position: relative;
	display: flex;
	align-self: stretch;
}

div.table table {
	flex-grow: 1;
	flex-basis: 0;
	align-self: start;
}

div.table div.dropdown {
	display: none;
	position: absolute;
	right: 0;
}

div.table:hover div.dropdown {
	display: inline-block;
}

"""
)

	def __init__(self,
		table,
		no_header = False,
		model = None,
		headers = None,
		format = lambda row, col, val: str(val),
		parse = lambda row, col, val: val,
		is_editable = lambda row, col: True,
		context_toolbar = None
	):
		"""Initialize a table. The passed argument may a 2-dimension
		Python list or an instance of table.Model.

		Format(row, col, val) and parse(row, col, val) arguments are functions,
		respectively to format and parse table values. Parse has to return None
		if the value cannot be parsed.

		is_editable(row, col) allows to test if a cell can be edited.

		context_toolbar is a component that will be displayed contextually
		for each line, usually a group of buttons. When clicked,
		get_context_row() can be used to get the row at this time.
		"""
		if model is None:
			model = self.MODEL
		Component.__init__(self, model)
		self.no_header = no_header
		if isinstance(table, TableModel):
			self.table = table
		else:
			self.table = ListTableModel(table)
		self.add_class("table")
		self.last_row = None
		self.last_col = None
		self.last_value = None
		self.shown = False
		self.headers = headers
		if self.headers is None:
			self.no_header = True
		self.format = format
		self.parse = parse
		self.is_editable = is_editable
		self.context_toolbar = context_toolbar
		if self.context_toolbar is not None:
			self.context_toolbar.parent = self
			self.set_attr("onmouseover", "table_over(this, event);")
		self.context_row = -1
		self.set_attr("onclick", f"table_on_click('{self.get_id()}', event);")

	def finalize(self, page):
		Component.finalize(self, page)
		if self.context_toolbar is not None:
			self.context_toolbar.finalize(page)

	def disable(self):
		self.add_class("disabled")

	def enable(self):
		self.remove_class("disabled")

	def get_context_row(self):
		"""Get the context row i.e. row where context tools has been used."""
		return self.context_row

	def add_row_class(self, row, cls):
		"""Add a class to a row."""
		if not self.no_header:
			cls += 1
		self.add_class(cls, id=f"{self.get_id()}-body", nth=row)

	def remove_row_class(self, row, cls):
		"""Remove a class from a row."""
		if not self.no_header:
			cls += 1
		self.remove_class(cls, id=f"{self.get_id()}-body", nth=row)

	def on_show(self):
		Component.on_show(self)
		self.table.add_observer(self)
		self.shown = True

	def on_hide(self):
		Component.on_hide(self)
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

	def get_context(self):
		return Context.ITEMBAR

	def gen_content(self, out):
		"""Generate the content of the table."""
		coln = self.table.get_column_count()
		out.write(f'<tbody id="{self.get_id()}-body">')

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

		out.write('</tbody>')

	def on_table_set(self, table):
		if self.online():
			buf = Buffer()
			self.gen_content(buf)
			self.set_content(str(buf), id=f"{self.get_id()}-table")

	def expands_horizontal(self):
		return True

	def expands_vertical(self):
		return True

	def gen(self, out):
		out.write('<div')
		self.gen_attrs(out)
		out.write(f'><table class="table" id="{self.get_id()}-table">')
		self.gen_content(out)
		out.write("</table>")
		if self.context_toolbar is not None:
			self.context_toolbar.gen(out)
		out.write("</div>")

	def refresh_cell(self, row, col):
		"""Referesh the content of a cell."""
		val = self.table.get_cell(row, col)
		act_row = row if self.no_header else row+1
		self.call("table_change", {
			"id": f"{self.get_id()}-table",
			"actions": [ ACTION_TR, act_row, ACTION_TD, col, ACTION_SET, 1 ],
			"values" : [ self.format(row, col, val) ]
		})

	def on_cell_set(self, table, row, col, val):
		"""Called by the model to update a cell value."""
		if self.online():
			self.refresh_cell(row, col)

	def on_row_append(self, table, vals):
		"""Called by the model to append a new row."""
		cnt = len(vals)
		row = self.table.get_row_count()-1
		self.call("table_change", {
			"id": f"{self.get_id()}-table",
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
			"id": f"{self.get_id()}-table",
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
			"id": f"{self.get_id()}-table",
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
			row, col = msg["row"], msg["col"]
			if row == 0 and not self.no_header:
				return
			if self.last_value is not None:
				self.check_edit(self.last_value)
			if not self.no_header:
				row -= 1
			if self.is_editable(row, col):
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

		# select the current context row
		elif action == "select":
			self.context_row = msg["idx"]
			if not self.no_header:
				self.context_row -= 1

		# default behaviour
		else:
			Component.receive(self, msg, handler)
