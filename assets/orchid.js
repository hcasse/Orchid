// Communication management



var ui_messages = [];
var ui_http = new XMLHttpRequest();
var converter = document.createElement('div')

function download() {
	if(this.readyState == 4) {
		if(this.status == 200) {
			node = document.getElementById(this.id);
			node.innerHTML = this.responseText;
		}
		else
			console.log("failed downloading.");
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

ui_http.onreadystatechange = function() {
	if(this.readyState == 4) {
		if(this.status != 200) {
			console.error("HTTP error: " + this.status);
		}
		else {
			//console.log("answer: " + this.responseText)
			ans = JSON.parse(this.responseText);
			for(const a of ans["answers"]) {
				//console.info("DEBUG:" + a);
				switch(a["type"]) {
				case "call":
					var f = window[a["fun"]];
					f(a["args"]);
					break;
				case "set":
					component = document.getElementById(a["id"]);
					component.style[a["attr"]] = a["val"];
					break;
				case "set-class":
					component = document.getElementById(a["id"]);
					component.className = a["classes"];
					console.log("set-class " + a["classes"] + " to " + a["id"]);
					break;
				case "set-attr":
					component = document.getElementById(a["id"]);
					component.setAttribute(a["attr"], a["val"]);
					break;
				case "remove-attr":
					component = document.getElementById(a["id"]);
					component.removeAttribute(a["attr"]);
					break;
				case 'set-content':
					component = document.getElementById(a["id"]);
					component.innerHTML = a["content"];
					break;
				case "quit":
					window.close();
					document.getElementsByTagName("body")[0].innerHTML = "<p>closed.</p>";
					break;
				case "download":
					req = new XMLHttpRequest();
					req.id = a["id"]
					req.onreadystatechange = download
					req.open("GET", a["path"], true);
					req.send();
					break;
				case "append":
					converter.innerHTML = a["content"]
					component = document.getElementById(a["id"]);
					for(const child of converter.children)
						component.append(child);
					while(converter.firstChild)
						converter.removeChild(converter.firstChild);
					break;
				case "clear":
					component = document.getElementById(a["id"]);
					while(component.firstChild)
						component.removeChild(component.firstChild);
					break;
				case "insert":
					converter.innerHTML = a["content"];
					component = document.getElementById(a["id"]);
					to = component.childNodes.item(a["pos"]);
					for(const child of converter.children)
						component.insertBefore(child, to);
					while(converter.firstChild)
						converter.removeChild(converter.firstChild);
					break;
				case "remove":
					component = document.getElementById(a["id"]);
					child = component.childNodes.item(a["child"]);
					component.removeChild(child);
					break;
				case "show-last":
					show_last(a["id"]);
					break;
				default:
					console.error("unknow command: " + a);
					break;
				}
			}
			if(ui_messages.length != 0)
				ui_complete();					
		}
	}
}

function ui_post(obj) {
	ui_messages.push(obj);
}

function ui_complete() {
	ui_http.open("POST", "ui", true);
	messages = ui_messages;
	ui_messages = [];
	ui_http.send(JSON.stringify({
		page: ui_page,
		messages: messages
	}));
}

function ui_send(obj) {
	console.log("DEBUG: send " + obj.id + " " + obj.action);
	ui_post(obj);
	ui_complete();
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
	ui_post({id: id, action: "click"});
}

function ui_ontopclick() {
	ui_send({id: "0", action: "click"});
}
