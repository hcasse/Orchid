
function list_index(id, event) {
	var item = event.target;
	var list = window.document.getElementById(id);
	if(item == list)
		return -1;
	while(item.parentNode != list)
		item = item.parentNode;
	var i = 0;
	while(item.previousSibling != null) {
		item = item.previousSibling;
		i++;
	}
	return i;
}

function list_on_click(id, event) {
	const index = list_index(id, event);
	if(index >= 0)
		ui_send({id: id, action: "select", item: index});
}

function list_on_context_menu(id, event) {
	event.preventDefault();
	const index = list_index(id, event);
	if(index >= 0)
		ui_send({id: id, action: "menu", item: index});
}

function list_select(args) {
	let list = window.document.getElementById(args.id);
	let index = args.index;
	let item = list.childNodes[index];
	item.classList.add("select");
}

function list_deselect(args) {
	let list = window.document.getElementById(args.id);
	let index = args.index;
	let item = list.childNodes[index];
	item.classList.remove("select");
}

function list_set(args) {
	let list = window.document.getElementById(args.id);
	let item = list.childNodes[args.index];
	item.innerHTML = args.content;
}

function list_clear(args) {
	let list = window.document.getElementById(args.id);
	while(list.firstChild != null)
		list.firstChild.remove();
}
