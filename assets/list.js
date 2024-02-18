
function list_on_click(id, event) {
	var item = event.target;
	ui_send({id: id, action: "select", item: item.id});
	console.log("list_on_clic");
	event.stopPropagation();
}
