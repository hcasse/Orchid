var ui_messages = [];
var ui_http = new XMLHttpRequest();

ui_http.onreadystatechange = function() {
	if(this.readyState == 4) {
		if(this.status != 200) {
			console.error("HTTP error: " + this.status);
		}
		else {
			/*console.log("answer: " + this.responseText)*/
			console.info(this.responseText);
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
					break;
				case "set-attr":
					component = document.getElementById(a["id"]);
					component.setAttribute(a["attr"], a["val"]);
					break;
				case "remove-attr":
					component = document.getElementById(a["id"]);
					component.removeAttribute(a["attr"]);
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
	ui_post(obj);
	ui_complete();
}

function ui_size(x) {
	if(typeof x == 'undefined' || x == "") {
		return 0;
	}
	else
		return parseFloat(x);
}

function ui_width(e) {
	s = getComputedStyle(e);
	return ui_size(s.width);
}

function ui_height(e) {
	s = getComputedStyle(e);
	return ui_size(s.height);
}

function ui_full_width(e) {
	s = getComputedStyle(e);
	return e.offsetWidth
		+  ui_size(s.marginLeft)
		+  ui_size(s.marginRight);
}

function ui_full_height(e) {
	s = getComputedStyle(e);
	return e.offsetHeight
		+  ui_size(s.marginTop)
		+  ui_size(s.marginBottom);
}

function ui_content_width(e) {
	s = getComputedStyle(e);
	return e.clientWidth
		 - ui_size(s.paddingLeft)
		 - ui_size(s.paddingRight)
}

function ui_content_height(e) {
	s = getComputedStyle(e);
	return e.clientHeight
		 - ui_size(s.paddingTop)
		 - ui_size(s.paddingBottom)
}

function ui_set_width(e, w) {
	s = getComputedStyle(e);
	w =	(w
		 - ui_size(s.borderLeftWidth)
		 - ui_size(s.borderRightWidth)
		 - ui_size(s.paddingLeft)
		 - ui_size(s.paddingRight)
		 - ui_size(s.marginLeft)
		 - ui_size(s.marginRight)
	) + "px";
	/*console.log("setting with of " + e.id + ": " + w);*/
	e.style.width = w;
}

function ui_set_height(e, h) {
	s = getComputedStyle(e);
	 h = (h
		 - ui_size(s.borderTopWidth)
		 - ui_size(s.borderBottomWidth)
		 - ui_size(s.paddingTop)
		 - ui_size(s.paddingBottom)
		 - ui_size(s.marginTop)
		 - ui_size(s.marginBottom)
	) + "px";
	/*console.log("setting height of " + e.id + ": " + h);*/
	e.style.height = h;
}

function ui_left_offset(e) {
	var s = getComputedStyle(e);
	return ui_size(s.borderLeftWidth)
		 + ui_size(s.paddingLeft)
		 + ui_size(s.marginLeft);
}

function ui_right_offset(e) {
	var s = getComputedStyle(e);
	return ui_size(s.borderRightWidth)
		 + ui_size(s.paddingRight)
		 + ui_size(s.marginRight);
}

function ui_top_offset(e) {
	var s = getComputedStyle(e);
	return ui_size(s.borderTopWidth)
		 + ui_size(s.paddingTop)
		 + ui_size(s.marginTop);
}

function ui_bottom_offset(e) {
	var s = getComputedStyle(e);
	return ui_size(s.borderBottomWidth)
		 + ui_size(s.paddingBottom)
		 + ui_size(s.marginBottom);
}

function ui_show_size(e) {
	var s = getComputedStyle(e);
	console.log("size of " + e.id + " = " + s.width + " x " + s.height);
	console.log("offset size of " + e.id + " = " + e.offsetWidth + " x " + e.offsetHeight);
	console.log("client size of " + e.id + " = " + e.clientWidth + " x " + e.clientHeight);
	console.log ("margin of " + e.id + " = "
		+ s.marginLeft + " "
		+ s.marginTop + " "
		+ s.marginRight + " "
		+ s.marginBottom + " ");
	console.log ("border of " + e.id + " = "
		+ s.borderLeftWidth + " "
		+ s.borderTopWidth + " "
		+ s.borderRightWidth + " "
		+ s.borderBottomWidth + " ");
	console.log ("padding of " + e.id + " = "
		+ s.paddingLeft + " "
		+ s.paddingTop + " "
		+ s.paddingRight + " "
		+ s.paddingBottom + " ");
}

function ui_open(addr) {
	window.open(addr);
}

function ui_close() {
	ui_send({id: "0", action: "close"});
	now = (new Date()).getTime();
	while(((new Date()).getTime() - now) < 250);
}

function ui_leave() {
	window.close();
}
