

function svg_append(args) {
	let svg = document.getElementById(args["id"]);
	let temp = svg.firstElementChild;
	temp.innerHTML = args["content"];
	while(temp.firstElementChild)
		svg.appendChild(temp.firstElementChild);
}

function svg_remove(args) {
	let obj = document.getElementById(args["id"]);
	obj.remove();
}

function svg_on_event(id, event) {
	console.log("event " + id + " " + event);
	ui_send({id: id, action: "event", event: event});
}

function svg_remove_all(args) {
	let svg = document.getElementById(args["id"]);
	let temp = svg.firstElementChild;
	while(svg.lastChild != temp)
		svg.removeChild(svg.lastChild);
}

function svg_size(args) {
	const id = args["id"];
	console.log("size of [" + id + "]");
	const svg = document.getElementById(id);
	const rect = svg.getBoundingClientRect();
	ui_send({id: id, action: "size", width: Math.round(rect.width), height: Math.round(rect.height)});
}
