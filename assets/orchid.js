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


// Popup management

var ui_popups = null;
var ui_popup = null;

function popup_show(args) {

	// activate the popup
	ui_popups = window.document.getElementById("ui-popups");
	ui_popup = window.document.getElementById(args.id);
	let comp = window.document.getElementById(args.comp);
	ui_popups.style.display = "block";
	ui_popup.style.display = args.display;

	// set the position
	let pr = ui_popup.getBoundingClientRect();
	let cr = comp.getBoundingClientRect();
	console.log("DEBUG: " + window.scrollX + ", " + window.scrollY);
	console.log("DEBUG: " + cr.left + "," + cr.top + "-" + cr.width + "x" + cr.height + " (" + cr.right + "," + cr.bottom + ")");
	switch(args.pos) {
	case 5:
		ui_popup.style.top = cr.bottom + "px";
		ui_popup.style.left = (cr.right - pr.width) + "px";
		break;
	}

	// fix position according to screen
	/*let sr = ui_pops.getBoundingClientRect();
	let cr = comp.getBoundingClientRect();
	if(cr.left < sr.left)
		cr.left = sr.left + "px";*/
}

function popup_hide() {
	ui_popups.style.display = "none";
	ui_popup.style.display = "none";
}

function popup_onclick(event) {
	if(event.target == ui_popups)
		popup_hide();
}

function popup_check(args) {
	const bw = document.body.clientWidth;
	const bh = document.body.clientHeight;
	console.log("DEBUG: " + bw + "x" + bh);
	const popup = window.document.getElementById(args.id);
	popup.style.display = args.display;
	const px = popup.clientLeft;
	const py = popup.clientTop;
	const pw = popup.clientWidth;
	const ph = popup.clientHeight
	console.log("DEBUG: " + px + "," + py + " " + pw + "x" + ph);
	const pb = popup.getBoundingClientRect();
	console.log("DEBUG: " + pb.left + "," + pb.top + " " + pb.width + "x" + pb.height);
	const dx = pb.left + pw - bw;
	if(dx > 0)
		popup.style.left = (pb.left - dx) + "px";
}

function popup_onresize(popup) {
	console.log("DEBUG: onresize " + popup);
}
