
function list_on_click(id, event) {
	var item = event.target;
	var list = window.document.getElementById(id);
	while(item.parentNode != list)
		item = item.parentNode;
	var i = 0;
	while(item.previousSibling != null) {
		item = item.previousSibling;
		i++;
	}
	ui_send({id: id, action: "select", item: i});
	/*console.log("list_on_clic");*/
	event.stopPropagation();
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
