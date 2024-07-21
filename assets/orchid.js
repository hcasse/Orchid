// Communication management

// https://developer.mozilla.org/fr/docs/Web/API/Window/requestIdleCallback

var ui_messages = [];
var ui_http = new XMLHttpRequest();
var ui_busy = true;
var converter = document.createElement('div')

function ui_index(node) {
	var i = 0;
	while(node.previousSibling != null) {
		node = node.previousSibling;
		i++;
	}
	return i;
}

function download() {
	if(this.readyState == 4) {
		if(this.status == 200) {
			node = document.getElementById(this.id);
			node.innerHTML = this.responseText;
		}
		else
			console.error("failed downloading.");
	}
}

function show_last(id) {
	const cont = document.getElementById(id);
	const elt = cont.lastChild
	if(elt == null)
		return;
	const etop = elt.offsetTop;
	const ebot = etop + elt.clientHeight;
	const ctop = cont.scrollTop;
	const cbot = ctop + cont.clientHeight;
	if(etop < ctop)
		cont.scrollTop -= ctop - etop;
	else if(ebot > cbot)
		cont.scrollTop += ebot - cbot;
}

function ui_component(msg) {
	let component = document.getElementById(msg.id);
	if(component == null)
		console.error(`no component with id ${msg.id}`);
	else {
		let nth = msg.nth;
		if(nth >= 0) {
			if(nth >= component.children.length) {
				console.error(`no ${nth}th component in ${msg.id} but only ${component.children.length}`);
				component = null;
			}
			else
				component = component.children[nth];
		}
	}
	return component;
}

ui_http.onreadystatechange = function() {
	if(this.readyState == 4) {
		if(this.status != 200) {
			console.error("HTTP error: " + this.status);
		}
		else {
			ans = JSON.parse(this.responseText);
			var component = null;
			for(let a of ans.answers) {
				//console.log("executing " + JSON.stringify(a));
				switch(a.type) {
				case "call":
					var f = window[a.fun];
					if(f == undefined)
						console.error(`cannot find function ${a.fun}`);
					else
						f(a.args);
					break;

				case "set-style":
					component = document.getElementById(a.id);
					component.style[a.attr] = a.val;
					break;
				case "set-class":
					component = document.getElementById(a.id);
					component.className = a.classes;
					break;
				case "add-class":
					component = ui_component(a);
					if(component != null)
						component.classList.add(a.class);
					break;
				case "remove-class":
					component = ui_component(a);
					if(component != null)
						component.classList.remove(a.class);
					break;
				case "set-attr":
					component = document.getElementById(a.id);
					component.setAttribute(a.attr, a.val);
					break;
				case "remove-attr":
					component = document.getElementById(a.id);
					component.removeAttribute(a.attr);
					break;

				case "quit":
					window.close();
					document.getElementsByTagName("body")[0].innerHTML = "<p>closed.</p>";
					break;
				case "download":
					req = new XMLHttpRequest();
					req.id = a.id
					req.onreadystatechange = download
					req.open("GET", a.path, true);
					req.send();
					break;

				case 'set-content':
					component = document.getElementById(a.id);
					component.innerHTML = a.content;
					break;
				case "clear":
					component = document.getElementById(a.id);
					while(component.firstChild)
						component.removeChild(component.firstChild);
					break;
				case "append":
					converter.innerHTML = a.content
					component = document.getElementById(a.id);
					for(const child of converter.children)
						component.append(child);
					while(converter.firstChild)
						converter.removeChild(converter.firstChild);
					break;
				case "insert":
					converter.innerHTML = a.content;
					component = document.getElementById(a.id);
					to = component.children[a.pos];
					component.insertBefore(converter.children[0], to);
					while(converter.firstChild)
						converter.firstChild.remove();
					break;
				case "remove":
					component = document.getElementById(a.id);
					child = component.children[a.pos];
					component.removeChild(child);
					break;

				case "show-last":
					show_last(a.id);
					break;

				case "model":
					for(const path of a.style_paths) {
						elem = document.createElement("link");
						elem.setAttribute("rel", "stylesheet");
						elem.setAttribute("href", path);
						document.head.appendChild(elem);
					}
					for(const path of a.script_paths) {
						elem = document.createElement("script");
						elem.setAttribute("src", path);
						document.head.appendChild(elem);
					}
					if(a.script)
						window.eval(a.script);
					if(a.style) {
						elem = document.createElement("style");
						elem.innerHTML = a.style;
						document.head.appendChild(elem);
					}
					break;

				default:
					console.error("unknown command: " + JSON.stringify(a));
					break;
				}
			}
			ui_release();
		}
	}
};

function ui_post(obj) {
	ui_messages.push(obj);
}

function ui_replace(msg) {
	let done = false;
	for(let i = 0; i < ui_messages.length; i++)
		if(ui_messages[i].id == msg.id && ui_messages[i].action == msg.action) {
			ui_messages[i] = msg;
			return;
		}
	ui_post(msg);
}

function ui_complete() {
	if(ui_messages.length == 0)
		return;
	ui_busy = true;
	ui_http.open("POST", "ui", true);
	let messages = ui_messages;
	ui_messages = [];
	ui_http.send(JSON.stringify({
		page: ui_page,
		messages: messages
	}));
}

function ui_release() {
	if(ui_messages.length != 0)
		ui_complete();
	else
		ui_busy = false;
}

function ui_send(obj) {
	ui_post(obj);
	if(!ui_busy)
		ui_complete();
}

function ui_hi() {
	console.log("hi!");
	ui_busy = false;
	ui_send({ id: "0", action: "hi" });
}


// Main actions

function ui_open(addr) {
	window.open(addr);
}

function ui_close() {
	ui_send({id: "0", action: "close"});
	now = (new Date()).getTime();
	while(((new Date()).getTime() - now) < 250);
}

function ui_onclick(id) {
	ui_send({id: id, action: "click"});
}


// Timer

ui_timers = new Map()

function ui_timer_start(args) {
	let id = args["id"];
	let time = args["time"];
	let periodic = args["periodic"];

	function callback() {
		ui_send({ id: id, action: "trigger" });
	}

	if(!ui_timers.has(id)) {
		if(periodic)
			ui_timers.set(id, setInterval(callback, time));
		else
			ui_timers.set(id, setTimeout(callback, time));
	}
}

function ui_timer_stop(args) {
	let id = args["id"];
	if(ui_timers.has(id)) {
		clearTimeout(ui_timers.get(id));
		ui_timers.delete(id);
	}
}
