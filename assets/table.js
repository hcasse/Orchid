function table_change(args) {
	const table = document.getElementById(args.id);
	var tr, td, cnt;
	var vali = 0;
	const actions = args.actions;
	const values = args.values;
	for(var i = 0; i < actions.length; i++) {
		switch(actions[i]) {
		case 0:
			tr = table.children[0].children[actions[++i]];
			break;
		case 1:
			td = tr.children[actions[++i]];
			break;
		case 2:
			cnt = actions[++i];
			for(var j = 0; j < cnt; j++) {
				td.innerHTML = values[vali++];
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

var table_edit = {
	cell: null,
	input: null,
	id: ""
}

function table_complete() {
	table_edit.cell.innerHTML = table_edit.input.value;
	table_edit.cell = null;
	ui_send({id: table_edit.id, action: "check", value: table_edit.input.value});
}

function table_onkeypress(event) {
	if(event.key == 'Enter')
		table_edit.input.blur();
}

function table_do_edit(args) {
	table_edit.cell.innerHTML = '<input id="table-edit" value="' + table_edit.cell.innerText + '" onblur="table_complete();" onkeypress="table_onkeypress(event);" oninput="table_on_change();"/>';
	table_edit.input = document.getElementById("table-edit");
	table_edit.input.focus();
	table_edit.input.select();
}

function table_set_ok(args) {
	table_edit.input.classList.remove("table-error");
}

function table_set_error(args) {
	table_edit.input.classList.add("table-error");
}


function table_on_change() {
	ui_send({id: table_edit.id, action: "test", value: table_edit.input.value});
}

function table_on_click(id, event) {
	var td = event.target;
	var tr = td.parentNode;
	var col;
	for(col = 0; col < tr.children.length && tr.children[col] !== td; col++);
	if(col == tr.children.length)
		return;
	var tbody = tr.parentNode;
	var row;
	for(row = 0; row < tbody.children.length && tbody.children[row] !== tr; row++);
	if(row == tbody.children.length)
		return;
	table_edit.cell = td;
	table_edit.id = id;
	ui_send({id: id, action: "is_editable", row: row, col: col});
}

function table_over(element, event) {
	var target = event.target;
	if(target.tagName == "TD")
		target = target.parentNode;
	if(target.tagName == "TR") {
		const i = ui_index(target);
		const div = element.parentNode;
		const popup = div.getElementsByTagName("DIV")[0];
		const y = target.getBoundingClientRect().top - element.getBoundingClientRect().top;
		popup.style.top = y + "px";
		ui_replace({id: element.id, action: "select", idx: i});
	}
}
