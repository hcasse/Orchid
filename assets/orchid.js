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
				switch(a["type"]) {
				case "call":
					var f = window[a["fun"]];
					f(a["args"]);
					break;
				case "set":
					component = document.getElementById(a["id"]);
					component.style[a["attr"]] = a["val"];
					break;
				case "class":
					component = document.getElementById(a["id"]);
					component.className = a["class"];
					break;
				case "add-class":
					component = document.getElementById(a["id"]);
					component.classList.add(a["class"]);
					break;
				case "remove-class":
					component = document.getElementById(a["id"]);
					component.classList.remove(a["class"]);
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

