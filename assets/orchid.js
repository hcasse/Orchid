var ui_messages = [];
var ui_http = new XMLHttpRequest();

ui_http.onreadystatechange = function() {
	if(this.readyState == 4) {
		console.info("ready to process");
		if(this.status != 200) {
			console.error("HTTP error: " + this.status);
		}
		else {
			console.log("answer: " + this.responseText)
			console.info(this.responseText);
			ans = JSON.parse(this.responseText);
			for(const a of ans["answers"]) {
				console.info("DEBUG:" + a);
				if(a["type"] == "call") {
					var f = window[a["fun"]];
					f(a["args"]);
				}
				else {
					component = document.getElementById(a["id"]);
					if(a["type"] == "set") {
						component.style[a["attr"]] = a["val"];
					}
					else if(a["type"] == "class") {
						component.className = a["class"];
					}
					else if(a["type"] == "add-class") {
						component.classList.add(a["class"]);
					}
					else if(a["type"] == "remove-class") {
						component.classList.remove(a["class"]);
					}
					else if(a['type'] == "set-attr") {
						component.setAttribute(a["attr"], a["val"]);
					}
					else if(a['type'] == "remove-attr") {
						component.removeAttribute(a["attr"]);						
					}
					else {
						console.error("unknow command: " + a)	
					}
				}
			}
		}
	}
}

function ui_post(obj) {
	ui_messages.push(obj);
}

function ui_complete() {
	ui_http.open("POST", "ui", true);
	ui_http.send(JSON.stringify({
		page: ui_page,
		messages: ui_messages
	}));
	ui_messages = [];
}

function ui_send(obj) {
	ui_post(obj);
	ui_complete();
}

