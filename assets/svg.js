

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
