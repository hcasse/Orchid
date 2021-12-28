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
				console.info(a);
				if(a["type"] == "set") {
					document.getElementById(a["id"]).style[a["attr"]] = a["val"];
				}
				else if(a["type"] == "call") {
					var f = window[a["fun"]];
					f(a["args"]);
				}
				else if(a["type"] == "class") {
					document.getElementById(a["id"]).className = a["class"];
				}
				else if(a["type"] == "add-class") {
					document.getElementById(a["id"]).classList.add(a["class"]);
				}
				else if(a["type"] == "remove-class") {
					document.getElementById(a["id"]).classList.remove(a["class"]);
				}
				else
					console.log("unknow command: " + a)
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

