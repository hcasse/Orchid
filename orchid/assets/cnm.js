const orc_cnm = {
	active: false,
	startX: 0,
	startY: 0,
	last: 0
};

function orc_cnm_push(element, event) {
	if(event.button !== 0)
		return;
	orc_cnm.dragging = true;
	orc_cnm.startX = event.clientX;
	orc_cnm.startY = event.clientY;
	orc_cnm.last = performance.now();
	//console.log("DEBUG: push " + element.id + ": " + orc_cnm.startX + ", " + orc_cnm.startY);
}

function orc_cnm_move(element, event, id) {
	if(!orc_cnm.dragging)
		return;
	const now = performance.now();
	if(now - orc_cnm.last < 100)
		return;
	orc_cnm.last = now;
	const dx = event.clientX - orc_cnm.startX;
	const dy = event.clientY - orc_cnm.startY;
	//console.log("DEBUG: move " + element.id + ": " + dx + ", " + dy);
	orc_cnm.startX = event.clientX;
	orc_cnm.startY = event.clientY;
	ui_send({ id: id, action: "move", dx: dx, dy: dy });
}

function orc_cnm_release(element, event) {
	if (!orc_cnm.dragging)
		return;
	orc_cnm.dragging = false;
	//console.log("DEBUG: released " + element.id + ": " + orc_cnm.startX + ", " + orc_cnm.startY)
}

function orc_cnm_cancel(element, event) {
	orc_cnm.dragging = false;
}

