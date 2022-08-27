// Communication management

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
				case "quit":
					window.close();
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



// Main actions

function ui_open(addr) {
	window.open(addr);
}

function ui_close() {
	ui_send({id: "0", action: "close"});
	//now = (new Date()).getTime();
	//while(((new Date()).getTime() - now) < 250);
}

/*function ui_leave() {
	window.close();
}*/

