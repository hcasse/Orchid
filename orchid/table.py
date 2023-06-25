"""Orchid module in charge of table display."""

from orchid import *
import orchid as orc

ACTION_TR	= 0		# TR number
ACTION_TD	= 1		# TD number
ACTION_SET	= 2		# set count
ACTION_REMOVE = 3	# no value
ACTION_APPEND = 4	# TD count
ACTION_INSERT = 5	# TD count

TABLE_MODEL = orc.Model(
	script="""
function table_change(args) {
	const table = document.getElementById(args.id);
	var tr, td, cnt;
	var vali = 0;
	const actions = args.actions;
	const values = args.values;
	console.log("DEBUG: actions = " + actions);
	console.log("DEBUG: actions = " + values);
	for(var i = 0; i < actions.length; i++) {
		switch(actions[i]) {
		case 0:
			tr = table.children[0].children[actions[++i]];
			console.log("DEBUG: ACTION_TR " + actions[i-1]);
			break;
		case 1:
			td = tr.children[actions[++i]];
			console.log("DEBUG: ACTION_TD " + actions[i-1]);
			break;
		case 2:
			cnt = actions[++i];
			for(var j = 0; j < cnt; j++) {
				td.innerHTML = values[vali++];
				console.log("DEBUG: ACTION_SET '" + values[vali- 1] + "' to " + td);
				td = td.nextElementSibling;
				if(td == null) {
					tr = tr.nextElementSibling;
					if(tr == null)
						td = null;
					else
						td = tr.children[0];
				}
			}
			break;
		case 3:
			const ntr = tr.nextElementSibling;
			tr.remove();
			tr = ntr;
			if(tr != null)
				td = null;
			else
				td = tr.children[0];
			break;
		case 4:
			cnt = actions[++i];
			tr = document.createElement("tr")
			table.children[0].append(tr);
			for(var j = 0; j < cnt; j++)
				tr.append(document.createElement("td"));
			td = tr.children[0];
			break;
		case 5:
			cnt = actions[++i];
			old = tr;
			tr = document.createElement("tr")
			table.children[0].insertBefore(tr, old);
			for(var j = 0; j < cnt; j++)
				tr.append(document.createElement("td"));
			td = tr.children[0];
			break;
		}
	}
}
"""
)

class Model(Subject):
	"""The model is used to define the lookup of the table in function
	the displayed cell. The returned value may be components, simple
	strings or None if there is nothing to display.

	The table the models applies to is stored in the table attribute.

	Notice that, after being displayed, all modifications to the table
	has to be performed throught the Model object."""

	def __init__(self):
		Subject.__init__(self)

	def get_header(self, column):
		"""Get the lookup of the given column header."""
		return None

	def get_column_count(self):
		"""Get the column count."""
		return 0

	def get_row_count(self):
		""""Get the row count."""
		return 0

	def get_cell(self, row, column):
		"""Get the lookup of the given cell."""
		return None

	def set_table(self, table):
		"""Called to change the table object."""
		if self.component != None:
			self.component.update_all()

	def set(self, row, column, value):
		"""Change the value of a table element."""
		if self.component != None:
			self.component.update_cell(row, column)

	def append_row(self, content):
		"""Append a new row to the table."""
		pass

	def insert_row(self, row, content):
		"""Insert the content at row position."""
		pass

	def remove_row(self, row):
		"""Remove the given row."""
		pass


class ListModel(Model):
	"""Table for a model based on Python list."""

	def __init__(self, table = None, column_count = None):
		Model.__init__(self)
		self.table = table
		self.component = None
		if column_count == None and table != None and table != []:
			self.column_count = len (table[0])
		else:
			self.column_count = column_count

	def get_header(self, column):
		return "Column %s" % column

	def get_column_count(self):
		return self.column_count

	def get_row_count(self):
		return len(self.table)

	def get_cell(self, row, column):
		return str(self.table[row][column])

	def set_table(self, table):
		self.table = table
		for obs in self.observers:
			obs.update_all()

	def set(self, row, column, value):
		self.table[row][column] = value
		for obs in self.observers:
			obs.update_cell(row, column)

	def append_row(self, content):
		self.table.append(content)
		for obs in self.observers:
			obs.update_append(content)

	def insert_row(self, row, content):
		self.table.insert(row, content)
		for obs in self.observers:
			obs.update_insert(row, content)

	def remove_row(self, row):
		del self.table[row]
		for obs in self.observers:
			obs.update_remove(row)
	

class View(orc.Component):
	"""Represents a table made of rows and columns."""

	def __init__(self,
			table,
			no_header = False,
			model = TABLE_MODEL
		):
		"""Initialize a table. The passed argument may a 2-dimension
		Python list or an instance of table.Model."""
		orc.Component.__init__(self, model)
		self.no_header = no_header
		if isinstance(table, Model):
			self.table = table
		else:
			self.table = ListModel(table)
		self.table.add_observer(self)
		self.add_class("table")
		self.set_style("display", "block")

	def gen(self, out):
		out.write("<table ")
		self.gen_attrs(out)
		out.write(">")
		coln = self.table.get_column_count()

		# if any, generate header
		if not self.no_header:
			out.write('<tr class="table-header">')
			for c in range(0, coln):
				out.write("<th>")
				self.gen_content(self.table.get_header(c), out)
				out.write("</th>")
			out.write("</tr>")

		# generate the content
		for r in range(0, self.table.get_row_count()):
			out.write("<tr>")
			for c in range(0, coln):
				out.write("<td>")
				self.gen_content(self.table.get_cell(r, c), out)
				out.write("</td>")
			out.write("</tr>")
		
		out.write("</table>")

	def gen_content(self, content, out):
		if content != None:
			if isinstance(content, orc.Component):
				content.gen(out)
			else:
				out.write(content)

	def get_table_model(self):
		"""Get the table model."""
		return self.table

	def update_all(self):
		# TODO
		pass

	def update_cell(self, row, col):
		"""Called by the model to update a cell value."""
		self.call("table_change", {
			"id": self.get_id(),
			"actions": [ ACTION_TR, row+1, ACTION_TD, col, ACTION_SET, 1 ],
			"values" : [ self.table.get_cell(row, col) ]
		})

	def update_append(self, content):
		"""Called by the model to append a new row."""
		cnt = len(content)
		self.call("table_change", {
			"id": self.get_id(),
			"actions": [ACTION_APPEND, cnt, ACTION_SET, cnt],
			"values": [str(x) for x in content]
		})

	def update_insert(self, row, content):
		"""Called by the model to insert a new row."""
		cnt = len(content)
		self.call("table_change", {
			"id": self.get_id(),
			"actions": [
				ACTION_TR, row+1,
				ACTION_INSERT, cnt,
				ACTION_SET, cnt
			],
			"values": [str(x) for x in content]
		})

	def update_remove(self, row):
		"""Called by the model to remove a row."""
		self.call("table_change", {
			"id": self.get_id(),
			"actions": [
				ACTION_TR, row+1,
				ACTION_REMOVE
			],
			"values": []
		})
